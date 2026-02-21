import React, { useEffect, useState } from 'react';
import { getVehicles, createVehicle, Vehicle, VehicleCreate } from '../api/vehicles';
import { Plus, Edit2, ShieldAlert } from 'lucide-react';

const Vehicles: React.FC = () => {
    const [vehicles, setVehicles] = useState<Vehicle[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Basic modal state
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState<VehicleCreate>({
        license_plate: '',
        make: '',
        model: '',
        year: new Date().getFullYear(),
        max_capacity_kg: 5000,
    });

    const fetchVehicles = async () => {
        try {
            const data = await getVehicles();
            setVehicles(data);
        } catch (err: any) {
            setError('Failed to fetch vehicles');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchVehicles();
    }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await createVehicle(formData);
            setIsModalOpen(false);
            fetchVehicles(); // refresh list
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to create vehicle');
        }
    };

    if (loading) return <div className="p-6">Loading vehicles...</div>;
    if (error) return <div className="p-6 text-danger-700">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-primary-900">Vehicle Registry</h2>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-center gap-2 bg-secondary-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-secondary-500/90 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    Add Vehicle
                </button>
            </div>

            {vehicles.length === 0 ? (
                <div className="bg-white p-12 rounded-xl border border-neutral-400/20 text-center">
                    <p className="text-neutral-400">No vehicles found in the registry.</p>
                </div>
            ) : (
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 overflow-hidden">
                    <table className="min-w-full divide-y divide-neutral-400/20">
                        <thead className="bg-neutral-50/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">License Plate</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Make/Model</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Year</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Capacity (kg)</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-neutral-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-neutral-400/20">
                            {vehicles.map((v) => (
                                <tr key={v.id} className="hover:bg-neutral-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-primary-900">{v.license_plate}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{v.make} {v.model}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{v.year}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{v.max_capacity_kg.toLocaleString()}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${v.status === 'Available' ? 'bg-success-600/10 text-success-600' :
                                                v.status === 'On Trip' ? 'bg-secondary-500/10 text-secondary-500' :
                                                    v.status === 'In Shop' ? 'bg-danger-700/10 text-danger-700' :
                                                        'bg-neutral-400/10 text-neutral-400'}
                    `}>
                                            {v.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button className="text-secondary-500 hover:text-primary-900 transition-colors mr-3" title="Edit Capacity/Status">
                                            <Edit2 className="w-4 h-4" />
                                        </button>
                                        {v.status !== 'Retired' && (
                                            <button className="text-danger-700 hover:text-danger-700/70 transition-colors" title="Retire Vehicle">
                                                <ShieldAlert className="w-4 h-4" />
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
                        <h3 className="text-lg font-bold text-primary-900 mb-4">Add New Vehicle</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-neutral-800">License Plate</label>
                                <input required type="text" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.license_plate} onChange={e => setFormData({ ...formData, license_plate: e.target.value })} />
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800">Make</label>
                                    <input required type="text" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.make} onChange={e => setFormData({ ...formData, make: e.target.value })} />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800">Model</label>
                                    <input required type="text" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.model} onChange={e => setFormData({ ...formData, model: e.target.value })} />
                                </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800">Year</label>
                                    <input required type="number" min="1990" max="2100" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.year} onChange={e => setFormData({ ...formData, year: parseInt(e.target.value) })} />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800">Capacity (kg)</label>
                                    <input required type="number" min="1" className="mt-1 block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.max_capacity_kg} onChange={e => setFormData({ ...formData, max_capacity_kg: parseInt(e.target.value) })} />
                                </div>
                            </div>
                            <div className="pt-4 flex justify-end gap-3">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-sm font-medium text-neutral-800 bg-neutral-50 hover:bg-neutral-400/10 rounded-lg">Cancel</button>
                                <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-primary-900 hover:bg-primary-900/90 rounded-lg">Save Vehicle</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Vehicles;
