import React from 'react';
import { Truck, ShieldCheck, Wrench, FileText, BarChart, LogOut, LayoutDashboard, Package, MapPin } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

interface SidebarProps {
    role: string | null;
}

const Sidebar: React.FC<SidebarProps> = ({ role }) => {
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        navigate('/login');
    };

    const isCustomer = role === 'Customer';

    return (
        <aside className="w-64 bg-primary-900 text-white min-h-screen flex flex-col transition-all duration-300">
            <div className="flex items-center gap-3 p-6 border-b border-primary-900/50 shadow-sm">
                <Truck className="w-8 h-8 text-secondary-500" />
                <h1 className="text-xl font-bold tracking-tight">FleetFlow</h1>
            </div>

            <nav className="flex-1 px-4 py-6 space-y-2">
                {isCustomer ? (
                    /* Customer-only navigation */
                    <>
                        <NavItem to="/tracking" icon={<Package />} label="Track Shipment" active={location.pathname === '/tracking'} />
                    </>
                ) : (
                    /* Management navigation */
                    <>
                        <NavItem to="/dashboard" icon={<LayoutDashboard />} label="Dashboard" active={location.pathname === '/dashboard' || location.pathname === '/'} />
                        <NavItem to="/vehicles" icon={<Truck />} label="Vehicles" active={location.pathname === '/vehicles'} />
                        {role !== 'Financial Analyst' && <NavItem to="/trips" icon={<MapPin />} label="Trips" active={location.pathname === '/trips'} />}
                        {role !== 'Dispatcher' && <NavItem to="/drivers" icon={<ShieldCheck />} label="Drivers" active={location.pathname === '/drivers'} />}
                        {role !== 'Dispatcher' && <NavItem to="/maintenance" icon={<Wrench />} label="Maintenance" active={location.pathname === '/maintenance'} />}
                        {role !== 'Dispatcher' && role !== 'Safety Officer' && <NavItem to="/expenses" icon={<FileText />} label="Expenses" active={location.pathname === '/expenses'} />}
                        {role !== 'Dispatcher' && role !== 'Safety Officer' && <NavItem to="/analytics" icon={<BarChart />} label="Analytics" active={location.pathname === '/analytics'} />}
                        <NavItem to="/tracking" icon={<Package />} label="Tracking" active={location.pathname === '/tracking'} />
                    </>
                )}
            </nav>

            <div className="p-4 border-t border-primary-900/50">
                <button onClick={handleLogout} className="flex items-center gap-3 w-full px-4 py-2 text-sm font-medium text-neutral-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                    <LogOut className="w-5 h-5" />
                    Logout
                </button>
            </div>
        </aside>
    );
};

interface NavItemProps {
    icon: React.ReactNode;
    label: string;
    to: string;
    active?: boolean;
}

const NavItem: React.FC<NavItemProps> = ({ icon, label, to, active }) => {
    return (
        <Link
            to={to}
            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-sm font-medium ${active
                ? 'bg-secondary-500 text-white'
                : 'text-neutral-400 hover:bg-white/10 hover:text-white'
                }`}
        >
            <span className="w-5 h-5">{icon}</span>
            {label}
        </Link>
    );
};

export default Sidebar;
