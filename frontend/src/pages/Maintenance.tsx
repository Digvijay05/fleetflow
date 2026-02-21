import React, { useEffect, useState } from 'react';
import { getMaintenanceLogs, createMaintenanceLog, updateMaintenanceLogStatus, MaintenanceLog, MaintenanceLogCreate } from '../api/maintenance';
import { getVehicles, Vehicle } from '../api/vehicles';
import { Wrench, Plus, CheckCircle2 } from 'lucide-react';

const Maintenance: React.FC = () => {
    const [logs, setLogs] = useState<MaintenanceLog[]>([]);
    const [vehicles, setVehicles] = useState<Vehicle[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState<MaintenanceLogCreate>({
        vehicle_id: '',
        type: 'Inspection',
        description: '',
        cost: 0,
        date: new Date().toISOString().split('T')[0],
    });

    const fetchData = async () => {
        try {
            const [logsData, vehiclesData] = await Promise.all([
                getMaintenanceLogs(),
                getVehicles(),
            ]);
            setLogs(logsData);
            setVehicles(vehiclesData);
        } catch (err: any) {
            setError('Failed to fetch maintenance records.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await createMaintenanceLog(formData);
            setIsModalOpen(false);
            fetchData(); // Refresh list to get updated logs and vehicle statuses
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to create maintenance record');
        }
    };

    const handleComplete = async (id: string) => {
        try {
            await updateMaintenanceLogStatus(id, { status: 'COMPLETED' });
            fetchData();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to complete record');
        }
    };

    if (loading) return <div className="p-6">Loading maintenance logs...</div>;
    if (error) return <div className="p-6 text-danger-700">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-primary-900">Maintenance Central</h2>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-center gap-2 bg-secondary-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-secondary-500/90 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    Log Service
                </button>
            </div>

            {logs.length === 0 ? (
                <div className="bg-white p-12 rounded-xl border border-neutral-400/20 text-center">
                    <p className="text-neutral-400">No maintenance history found.</p>
                </div>
            ) : (
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 overflow-hidden">
                    <table className="min-w-full divide-y divide-neutral-400/20">
                        <thead className="bg-neutral-50/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Vehicle ID</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Description</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Estimated Cost</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-right text-xs font-semibold text-neutral-400 uppercase tracking-wider">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-neutral-400/20">
                            {logs.map((log) => (
                                <tr key={log.id} className="hover:bg-neutral-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{new Date(log.date).toLocaleDateString()}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-primary-900">{log.vehicle_id.substring(0, 8)}...</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800 truncate max-w-[200px]">{log.description}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">${log.cost.toLocaleString()}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${log.status === 'COMPLETED' ? 'bg-success-600/10 text-success-600' :
                                                log.status === 'IN_PROGRESS' ? 'bg-warning-500/10 text-warning-500' :
                                                    'bg-secondary-500/10 text-secondary-500'}
                    `}>
                                            {log.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        {log.status !== 'COMPLETED' && (
                                            <button onClick={() => handleComplete(log.id)} className="text-success-600 hover:text-success-600/70 transition-colors flex items-center justify-end w-full gap-2" title="Mark Completed">
                                                <CheckCircle2 className="w-4 h-4" />
                                                Complete
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-primary-900/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl p-6 w-full max-w-md">
                        <h3 className="text-lg font-bold text-primary-900 mb-4 items-center flex gap-2"><Wrench className="w-5 h-5 text-secondary-500" /> Log Maintenance</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Select Vehicle</label>
                                <select required className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2 bg-white" value={formData.vehicle_id} onChange={e => setFormData({ ...formData, vehicle_id: e.target.value })}>
                                    <option value="">-- Choose a Vehicle --</option>
                                    {vehicles.filter(v => v.status !== 'Retired').map(v => (
                                        <option key={v.id} value={v.id}>{v.license_plate} - {v.make}</option>
                                    ))}
                                </select>
                                <p className="text-xs text-secondary-500 mt-1">Note: This will place the vehicle 'In Shop'.</p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Maintenance Type</label>
                                <select required className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2 bg-white" value={formData.type} onChange={e => setFormData({ ...formData, type: e.target.value as any })}>
                                    <option value="Oil Change">Oil Change</option>
                                    <option value="Tire Replacement">Tire Replacement</option>
                                    <option value="Engine Repair">Engine Repair</option>
                                    <option value="Inspection">Inspection</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Issue Description</label>
                                <textarea required rows={3} className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.description} onChange={e => setFormData({ ...formData, description: e.target.value })} placeholder="e.g., Routine oil change and brake inspection" />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Estimated Cost ($)</label>
                                <input required type="number" min="0" step="0.01" className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.cost || ''} onChange={e => setFormData({ ...formData, cost: parseFloat(e.target.value) })} />
                            </div>

                            <div className="pt-4 flex justify-end gap-3 border-t border-neutral-400/20">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-sm font-medium text-neutral-800 bg-neutral-50 hover:bg-neutral-400/10 rounded-lg transition-colors">Cancel</button>
                                <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-secondary-500 hover:bg-secondary-500/90 rounded-lg transition-colors">Submit Log</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Maintenance;
