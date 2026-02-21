import React, { useEffect, useState } from 'react';
import { getDrivers, createDriver, Driver, DriverCreate } from '../api/drivers';
import { UserPlus, Edit2, UserX } from 'lucide-react';

const Drivers: React.FC = () => {
    const [drivers, setDrivers] = useState<Driver[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Basic modal state
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState<DriverCreate>({
        name: '',
        license_number: '',
        license_expiry: new Date(new Date().setFullYear(new Date().getFullYear() + 1)).toISOString().split('T')[0],
    });

    const fetchDrivers = async () => {
        try {
            const data = await getDrivers();
            setDrivers(data);
        } catch (err: any) {
            setError('Failed to fetch drivers');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDrivers();
    }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await createDriver(formData);
            setIsModalOpen(false);
            fetchDrivers(); // refresh list
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to create driver');
        }
    };

    if (loading) return <div className="p-6">Loading drivers...</div>;
    if (error) return <div className="p-6 text-danger-700">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-primary-900">Driver Directory</h2>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-center gap-2 bg-secondary-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-secondary-500/90 transition-colors"
                >
                    <UserPlus className="w-4 h-4" />
                    Add Driver
                </button>
            </div>

            {drivers.length === 0 ? (
                <div className="bg-white p-12 rounded-xl border border-neutral-400/20 text-center">
                    <p className="text-neutral-400">No drivers currently in the directory.</p>
                </div>
            ) : (
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 overflow-hidden">
                    <table className="min-w-full divide-y divide-neutral-400/20">
                        <thead className="bg-neutral-50/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Name</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">License Number</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Expiry</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-neutral-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-neutral-400/20">
                            {drivers.map((d) => (
                                <tr key={d.id} className="hover:bg-neutral-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-primary-900">{d.name}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{d.license_number}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{new Date(d.license_expiry).toLocaleDateString()}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${d.status === 'On Duty' ? 'bg-success-600/10 text-success-600' :
                                                d.status === 'On Trip' ? 'bg-secondary-500/10 text-secondary-500' :
                                                    d.status === 'Suspended' ? 'bg-danger-700/10 text-danger-700' :
                                                        'bg-neutral-400/10 text-neutral-400'}
                    `}>
                                            {d.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button className="text-secondary-500 hover:text-primary-900 transition-colors mr-3" title="Edit Status">
                                            <Edit2 className="w-4 h-4" />
                                        </button>
                                        {d.status !== 'Suspended' && (
                                            <button className="text-danger-700 hover:text-danger-700/70 transition-colors" title="Suspend Driver">
                                                <UserX className="w-4 h-4" />
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Basic Create Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-primary-900/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl p-6 w-full max-w-md">
                        <h3 className="text-lg font-bold text-primary-900 mb-4">Register New Driver</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-neutral-800">Full Name</label>
                                <input required type="text" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-neutral-800">License Number</label>
                                <input required type="text" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.license_number} onChange={e => setFormData({ ...formData, license_number: e.target.value })} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-neutral-800">License Expiry</label>
                                <input required type="date" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.license_expiry} onChange={e => setFormData({ ...formData, license_expiry: e.target.value })} />
                            </div>
                            <div className="pt-4 flex justify-end gap-3">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-sm font-medium text-neutral-800 bg-neutral-50 hover:bg-neutral-400/10 rounded-lg">Cancel</button>
                                <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-primary-900 hover:bg-primary-900/90 rounded-lg">Save Driver</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Drivers;
