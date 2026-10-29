import { NavLink } from 'react-router'

// Menu items without a page yet fall through to the "*" route in App.
const MENU_ITEMS = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'My Reviews', path: '/my-reviews' },
  { label: 'Submit Review', path: '/submit-review' },
  { label: 'Reviews', path: '/reviews' },
  { label: 'Employees', path: '/employees' },
]

export default function Menu() {
  // NavLink marks the item matching the current URL as active, so no local state is needed.
  return (
    <aside className="sidebar">
      <div className="brand">Testleaf</div>
      <nav>
        {MENU_ITEMS.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => (isActive ? 'menu-item active' : 'menu-item')}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
