import { useState } from 'react';
import { Truck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const navigate = useNavigate();

    const [error, setError] = useState('');

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        if (submitting) return; // double-submit guard
        setSubmitting(true);
        setError('');
        try {
            const data = await login(email, password);
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('role', data.role);

            // Role-aware redirect
            if (data.role === 'Customer') {
                navigate('/tracking');
            } else {
                navigate('/dashboard');
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="min-h-screen bg-primary-900 flex flex-col justify-center items-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="flex justify-center">
                    <Truck className="w-12 h-12 text-secondary-500" />
                </div>
                <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
                    Sign in to FleetFlow
                </h2>
                <p className="mt-2 text-center text-sm font-medium text-neutral-400">
                    Command center for your logistics platform
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white py-8 px-4 shadow-xl sm:rounded-xl border border-neutral-400/20 sm:px-10">
                    {error && (
                        <div className="mb-4 bg-danger-700/10 border border-danger-700/30 text-danger-700 px-4 py-3 rounded-lg text-sm">
                            {error}
                        </div>
                    )}
                    <form className="space-y-6" onSubmit={handleLogin}>
                        <div>
                            <label className="block text-sm font-medium text-primary-900">
                                Email address
                            </label>
                            <div className="mt-2">
                                <input
                                    type="email"
                                    required
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="appearance-none block w-full px-4 py-3 border border-neutral-400/30 rounded-lg shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 text-sm transition-colors bg-neutral-50"
                                    placeholder="admin@fleetflow.com"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-primary-900">
                                Password
                            </label>
                            <div className="mt-2">
                                <input
                                    type="password"
                                    required
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="appearance-none block w-full px-4 py-3 border border-neutral-400/30 rounded-lg shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-secondary-500 focus:border-secondary-500 text-sm transition-colors bg-neutral-50"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <div className="flex items-center">
                                <input
                                    id="remember-me"
                                    type="checkbox"
                                    className="h-4 w-4 text-secondary-500 focus:ring-secondary-500 border-neutral-400/30 rounded transition-colors"
                                />
                                <label htmlFor="remember-me" className="ml-2 block text-sm font-medium text-neutral-800">
                                    Remember me
                                </label>
                            </div>

                            <div className="text-sm font-medium">
                                <a href="#" className="text-secondary-500 hover:text-secondary-500/80 transition-colors">
                                    Forgot password?
                                </a>
                            </div>
                        </div>

                        <div>
                            <button
                                type="submit"
                                disabled={submitting}
                                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-bold text-white bg-primary-900 hover:bg-primary-900/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-900 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {submitting ? 'Signing in...' : 'Sign In'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
