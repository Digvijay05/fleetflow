import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Truck, ArrowLeft } from 'lucide-react';

const NotFoundFallback: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-8">
            <div className="text-center space-y-6 max-w-lg">
                <div className="mx-auto w-20 h-20 bg-primary-900/10 rounded-full flex items-center justify-center">
                    <Truck className="w-10 h-10 text-primary-900" />
                </div>
                <h1 className="text-7xl font-extrabold text-primary-900">404</h1>
                <h2 className="text-xl font-semibold text-primary-900">Page Not Found</h2>
                <p className="text-sm text-neutral-400 max-w-sm mx-auto">
                    The route you're looking for doesn't exist or has been moved. Let's get you back on track.
                </p>
                <button
                    onClick={() => navigate('/')}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-secondary-500 text-white rounded-lg text-sm font-medium hover:bg-secondary-500/90 transition-colors"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Dashboard
                </button>
            </div>
        </div>
    );
};

export default NotFoundFallback;
