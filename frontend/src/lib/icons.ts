/**
 * METHEAN icon system.
 *
 * Single re-export surface for Lucide React icons used in the app.
 * Re-exporting here (rather than importing lucide-react in every
 * component) means we can swap the underlying library or adjust
 * defaults globally without touching consumers.
 *
 * Defaults applied across the product (set by the <Icon> wrapper
 * in components/ui/Icon.tsx):
 *   - strokeWidth: 1.5
 *   - color: currentColor (inherits from parent text color)
 *   - aria-hidden: true (icons are decorative by default; consumers
 *     that need semantic icons pass a label themselves)
 *
 * Use the <Icon> wrapper for the standard look; reach for the raw
 * lucide-react exports only for one-off custom sizing.
 */

export {
  ChevronRight,
  ChevronLeft,
  ChevronUp,
  ChevronDown,
  ArrowRight,
  ArrowLeft,
  ArrowUp,
  ArrowDown,
  ArrowUpRight,
  Check,
  CheckCircle2,
  X,
  XCircle,
  Plus,
  Minus,
  Search,
  Menu,
  MoreHorizontal,
  MoreVertical,
  Settings,
  Info,
  AlertTriangle,
  AlertCircle,
  HelpCircle,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Play,
  Pause,
  Square,
  SkipForward,
  Send,
  MessageCircle,
  Edit3,
  Trash2,
  Download,
  Upload,
  ExternalLink,
  Eye,
  EyeOff,
  Lock,
  Unlock,
  User,
  Users,
  BookOpen,
  Book,
  Bookmark,
  Star,
  Heart,
  Calendar,
  CalendarDays,
  Clock,
  Home,
  Compass,
  Map,
  MapPin,
  Trophy,
  Award,
  Target,
  Sparkles,
  TrendingUp,
  TrendingDown,
  Activity,
  BarChart3,
  PieChart,
  Loader2,
  RefreshCw,
  Bell,
  BellOff,
  Filter,
  SlidersHorizontal,
  Copy,
  Share2,
  Link as LinkIcon,
  FileText,
  FileCheck2,
  Folder,
  FolderOpen,
  Hash,
  AtSign,
  Mail,
  Shield,
  ShieldCheck,
  ShieldPlus,
  KeyRound,
  LogIn,
  LogOut,
  ChevronsUpDown,
  PanelLeft,
  PanelRight,
  Maximize2,
  Minimize2,
  Layers3,
  Wrench,
  Lightbulb,
} from "lucide-react";

export type { LucideProps, LucideIcon } from "lucide-react";
