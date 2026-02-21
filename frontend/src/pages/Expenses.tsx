import React, { useEffect, useState } from 'react';
import { getExpenses, createExpense, Expense, ExpenseCreate } from '../api/expenses';
import { getVehicles, Vehicle } from '../api/vehicles';
import { getTrips, Trip } from '../api/trips';
import { FileText, Plus, DollarSign } from 'lucide-react';

const Expenses: React.FC = () => {
    const [expenses, setExpenses] = useState<Expense[]>([]);
    const [vehicles, setVehicles] = useState<Vehicle[]>([]);
    const [trips, setTrips] = useState<Trip[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState<ExpenseCreate>({
        vehicle_id: '',
        trip_id: '',
        fuel_liters: 0,
        fuel_cost: 0,
        date: new Date().toISOString().split('T')[0],
    });

    const fetchData = async () => {
        try {
            const [expensesData, vehiclesData, tripsData] = await Promise.all([
                getExpenses(),
                getVehicles(),
                getTrips(),
            ]);
            setExpenses(expensesData);
            setVehicles(vehiclesData);
            setTrips(tripsData);
        } catch (err: any) {
            setError('Failed to fetch financial data.');
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
            await createExpense(formData);
            setIsModalOpen(false);
            fetchData();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to log expense (ensure trip matches vehicle active routing).');
        }
    };

    if (loading) return <div className="p-6">Loading financials...</div>;
    if (error) return <div className="p-6 text-danger-700">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-primary-900">Operational Expenses</h2>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-center gap-2 bg-secondary-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-secondary-500/90 transition-colors"
                >
                    <Plus className="w-4 h-4" />
                    Log Expense
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6 flex items-start gap-4">
                    <div className="p-4 rounded-xl bg-danger-700/10 text-danger-700">
                        <DollarSign className="w-6 h-6" />
                    </div>
                    <div>
                        <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-wide">Total Expenses</h3>
                        <p className="text-2xl font-bold text-primary-900 mt-1">
                            ${expenses.reduce((sum, e) => sum + e.fuel_cost, 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </p>
                    </div>
                </div>
            </div>

            {expenses.length === 0 ? (
                <div className="bg-white p-12 rounded-xl border border-neutral-400/20 text-center">
                    <p className="text-neutral-400">No expenses recorded yet.</p>
                </div>
            ) : (
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 overflow-hidden">
                    <table className="min-w-full divide-y divide-neutral-400/20">
                        <thead className="bg-neutral-50/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Vehicle ID</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Trip ID</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Fuel (L)</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-neutral-400 uppercase tracking-wider">Cost</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-neutral-400/20">
                            {expenses.map((expense) => (
                                <tr key={expense.id} className="hover:bg-neutral-50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{new Date(expense.date).toLocaleDateString()}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-primary-900">{expense.vehicle_id.substring(0, 8)}...</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{expense.trip_id.substring(0, 8)}...</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-800">{expense.fuel_liters.toLocaleString()} L</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-danger-700">
                                        ${expense.fuel_cost.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
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
                        <h3 className="text-lg font-bold text-primary-900 mb-4 items-center flex gap-2"><FileText className="w-5 h-5 text-secondary-500" /> Log Expense</h3>
                        <form onSubmit={handleCreate} className="space-y-4">

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Date</label>
                                <input required type="date" className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2 bg-white" value={formData.date} onChange={e => setFormData({ ...formData, date: e.target.value })} />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Select Vehicle</label>
                                <select required className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2 bg-white" value={formData.vehicle_id} onChange={e => setFormData({ ...formData, vehicle_id: e.target.value })}>
                                    <option value="">-- Choose a Vehicle --</option>
                                    {vehicles.map(v => (
                                        <option key={v.id} value={v.id}>{v.license_plate} - {v.make}</option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Associated Trip ID</label>
                                <select required className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2 bg-white" value={formData.trip_id} onChange={e => setFormData({ ...formData, trip_id: e.target.value })}>
                                    <option value="">-- Choose Active Trip --</option>
                                    {trips.filter(t => t.vehicle_id === formData.vehicle_id).map(t => (
                                        <option key={t.id} value={t.id}>{t.origin} → {t.destination} ({t.status})</option>
                                    ))}
                                </select>
                                <p className="text-xs text-neutral-400 mt-1">Must match the selected vehicle above.</p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Fuel Log Amount (Liters)</label>
                                <input required type="number" min="0" step="0.1" className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.fuel_liters || ''} onChange={e => setFormData({ ...formData, fuel_liters: parseFloat(e.target.value) })} />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Fuel Cost ($)</label>
                                <input required type="number" min="0" step="0.01" className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.fuel_cost || ''} onChange={e => setFormData({ ...formData, fuel_cost: parseFloat(e.target.value) })} />
                            </div>

                            <div className="pt-4 flex justify-end gap-3 border-t border-neutral-400/20">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-sm font-medium text-neutral-800 bg-neutral-50 hover:bg-neutral-400/10 rounded-lg transition-colors">Cancel</button>
                                <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-secondary-500 hover:bg-secondary-500/90 rounded-lg transition-colors">Submit Expense</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Expenses;
