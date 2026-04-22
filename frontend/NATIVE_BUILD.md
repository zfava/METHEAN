# METHEAN Native Build Guide

## Prerequisites

- Node.js 20+
- Xcode 15+ (macOS only, for iOS builds)
- Android Studio (for Android builds)
- JDK 17 (for Android builds)
- Apple Developer account ($99/year, for App Store)
- Google Play Console account ($25 one-time, for Play Store)

## Quick Start

```bash
cd frontend

# Install dependencies (includes Capacitor)
npm install

# Add native platforms (one-time)
npx cap add ios
npx cap add android

# Build and sync
npm run build:ios       # Export + sync to iOS
npm run build:android   # Export + sync to Android

# Open in IDE
npm run cap:ios         # Opens Xcode
npm run cap:android     # Opens Android Studio
```

## iOS Setup

### 1. Apple Developer Portal
- Create an App ID: `io.methean.app`
- Enable capabilities: Push Notifications, Associated Domains
- Create provisioning profiles (Development + Distribution)

### 2. Xcode Configuration
After `npx cap add ios`:
- Open `ios/App/App.xcworkspace` in Xcode
- Set deployment target: iOS 16.0
- Set device family: Universal (iPhone + iPad)
- Set orientations: Portrait (iPhone), All (iPad)
- Enable automatic signing with your team

### 3. Info.plist
Copy entries from `ios-config/Info.plist.additions` into `ios/App/App/Info.plist`:
- NSCameraUsageDescription
- NSPhotoLibraryUsageDescription
- NSFaceIDUsageDescription
- ITSAppUsesNonExemptEncryption (false)

### 4. Privacy Manifest
Copy `ios-config/PrivacyInfo.xcprivacy` into `ios/App/App/`

### 5. Build
```bash
npm run build:ios
npm run cap:ios  # Opens Xcode
# In Xcode: Product > Archive > Distribute to App Store
```

## Android Setup

### 1. Signing
```bash
# Generate release keystore (one-time, keep safe!)
keytool -genkey -v -keystore methean-release.keystore \
  -alias methean -keyalg RSA -keysize 2048 -validity 10000

# Copy template and fill in values
cp android-config/keystore.properties.template android/keystore.properties
```

### 2. Permissions
After `npx cap add android`, verify permissions in `android/app/src/main/AndroidManifest.xml`.
Compare with `android-config/permissions.xml`.

### 3. Build
```bash
# Debug APK
npm run build:android
npm run cap:android  # Opens Android Studio

# Release AAB (for Play Store)
npm run build:android:release
# Output: android/app/build/outputs/bundle/release/app-release.aab
```

## Version Management

```bash
# Bump patch: 0.1.0 → 0.1.1
npm run version:bump patch

# Bump minor: 0.1.0 → 0.2.0
npm run version:bump minor

# Bump major: 0.1.0 → 1.0.0
npm run version:bump major
```

Updates: package.json, iOS Info.plist, Android build.gradle

## CI/CD

Native builds run automatically on tagged releases via `.github/workflows/native-builds.yml`:

```bash
git tag v0.1.1
git push --tags
# → Android AAB and iOS archive uploaded as GitHub Actions artifacts
```

## App Store Submission Checklist

### iOS (App Store Connect)
- [ ] App icon (1024x1024) — generated in `assets/`
- [ ] Screenshots for 4 device sizes (see `store-metadata/app-store-description.md`)
- [ ] App description and keywords
- [ ] Privacy policy URL: https://methean.app/privacy
- [ ] Age rating: 4+
- [ ] Privacy manifest included
- [ ] Export compliance: non-exempt encryption (HTTPS only)

### Android (Play Console)
- [ ] App icon — generated in `assets/`
- [ ] Feature graphic (1024x500)
- [ ] Screenshots for phone and tablet
- [ ] Store listing description
- [ ] Privacy policy URL
- [ ] Content rating questionnaire
- [ ] Data safety form (see `store-metadata/data-safety.md`)
- [ ] Target API level: 34+
- [ ] Signed AAB uploaded

## Security Notes

**Never commit to git:**
- `android/keystore.properties`
- `*.keystore` files
- Apple signing certificates
- FCM service account JSON

These are in `.gitignore`. Store secrets in CI environment variables.
