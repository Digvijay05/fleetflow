import React from 'react';
import Sidebar from './Sidebar';

interface LayoutProps {
    children: React.ReactNode;
    role: string | null;
}

const Layout: React.FC<LayoutProps> = ({ children, role }) => {
    return (
        <div className="flex bg-neutral-50 min-h-screen font-sans">
            <Sidebar role={role} />
            <main className="flex-1 flex flex-col min-h-screen overflow-y-auto bg-neutral-50 px-8 py-6">
                {/* Basic Header */}
                <header className="flex items-center justify-between mb-8 pb-4 border-b border-neutral-400/20">
                    <div>
                        <h1 className="text-2xl tracking-tight font-bold text-primary-900">Dashboard</h1>
                        <p className="text-sm font-medium text-neutral-400 mt-1">Overview of your fleet operations</p>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="flex flex-col items-end">
                            <span className="text-sm font-bold text-primary-900">User</span>
                            <span className="text-xs font-medium text-neutral-400 uppercase">{role || 'GUEST'}</span>
                        </div>
                        <div className="w-10 h-10 rounded-full bg-secondary-500 flex items-center justify-center text-white font-bold">
                            U
                        </div>
                    </div>
                </header>

                <div className="flex-1 pb-8">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
