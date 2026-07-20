interface IconProps {
  name: string
  filled?: boolean
  className?: string
}

const iconMap: Record<string, string> = {
  add: 'add',
  add_task: 'add_task',
  analytics: 'analytics',
  arrow_back: 'arrow_back',
  arrow_forward: 'arrow_forward',
  boy: 'boy',
  call: 'call',
  chevron_right: 'chevron_right',
  child_care: 'child_care',
  directions_run: 'directions_run',
  eco: 'eco',
  edit_note: 'edit_note',
  expand_more: 'expand_more',
  face: 'face',
  flashlight: 'flashlight_on',
  fitness_center: 'fitness_center',
  flag: 'flag',
  girl: 'girl',
  home: 'home',
  history: 'history',
  info: 'info',
  lightbulb: 'lightbulb',
  location_on: 'location_on',
  map: 'map',
  map_pin_2: 'location_on',
  menu: 'menu',
  men: 'man',
  my_location: 'my_location',
  near_me: 'near_me',
  nutrition: 'restaurant',
  accessibility_new: 'accessibility_new',
  arrow_up_double: 'vertical_align_top',
  chat: 'chat',
  groups: 'groups',
  open_in_new: 'open_in_new',
  run: 'directions_run',
  schedule: 'schedule',
  search: 'search',
  seedling: 'eco',
  sparkling: 'auto_awesome',
  sports_score: 'sports_score',
  straighten: 'straighten',
  trending_up: 'trending_up',
  user_smile: 'face',
  women: 'woman',
  footprint: 'footprint',
  tree: 'park',
  home_4: 'fitness_center',
  community: 'groups',
  football: 'sports_soccer',
}

export function Icon({ name, filled = false, className = '' }: IconProps) {
  const iconName = iconMap[name] ?? name
  return (
    <span
      aria-hidden="true"
      className={`material-symbols-rounded ${filled ? 'material-symbols-filled' : ''} ${className}`}
    >
      {iconName}
    </span>
  )
}
