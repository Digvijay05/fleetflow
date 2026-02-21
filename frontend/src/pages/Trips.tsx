import React, { useEffect, useState } from 'react';
import { getTrips, createTrip, updateTripStatus, Trip, TripCreate, TripUpdateStatus } from '../api/trips';
import { getVehicles, Vehicle } from '../api/vehicles';
import { getDrivers, Driver } from '../api/drivers';
import { MapPin, Navigation, CheckCircle, Package } from 'lucide-react';

const Trips: React.FC = () => {
    const [trips, setTrips] = useState<Trip[]>([]);
    const [vehicles, setVehicles] = useState<Vehicle[]>([]);
    const [drivers, setDrivers] = useState<Driver[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState<TripCreate>({
        vehicle_id: '',
        driver_id: '',
        origin: '',
        destination: '',
        cargo_weight: 0,
    });

    const fetchData = async () => {
        try {
            const [tripsData, vehiclesData, driversData] = await Promise.all([
                getTrips(),
                getVehicles(),
                getDrivers(),
            ]);
            setTrips(tripsData);
            setVehicles(vehiclesData);
            setDrivers(driversData);
        } catch (err: any) {
            setError('Failed to fetch dispatcher data.');
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
            await createTrip(formData);
            setIsModalOpen(false);
            fetchData(); // Refresh all to get updated Vehicle/Driver statuses
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Dispatch failed: Check capacity overrides or availability constraints.');
        }
    };

    const handleUpdateStatus = async (id: string, newStatus: TripUpdateStatus['status']) => {
        try {
            await updateTripStatus(id, { status: newStatus });
            fetchData();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to update trip status');
        }
    };

    if (loading) return <div className="p-6">Loading dispatch board...</div>;
    if (error) return <div className="p-6 text-danger-700">{error}</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-primary-900">Trip Dispatcher</h2>
                <button
                    onClick={() => setIsModalOpen(true)}
                    className="flex items-center gap-2 bg-secondary-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-secondary-500/90 transition-colors"
                >
                    <Navigation className="w-4 h-4" />
                    New Dispatch
                </button>
            </div>

            <div className="grid grid-cols-1 gap-4">
                {trips.length === 0 ? (
                    <div className="bg-white p-12 rounded-xl border border-neutral-400/20 text-center">
                        <p className="text-neutral-400">No active or historical trips.</p>
                    </div>
                ) : (
                    trips.map((t) => (
                        <div key={t.id} className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6 flex flex-col md:flex-row gap-6 md:items-center justify-between">
                            <div className="flex-1 space-y-4">
                                <div className="flex items-center gap-3">
                                    <span className={`px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${t.status === 'COMPLETED' ? 'bg-success-600/10 text-success-600' :
                                            t.status === 'DISPATCHED' ? 'bg-secondary-500/10 text-secondary-500' :
                                                t.status === 'CANCELLED' ? 'bg-danger-700/10 text-danger-700' :
                                                    'bg-neutral-400/10 text-neutral-400'}
                    `}>
                                        {t.status}
                                    </span>
                                    <span className="text-sm text-neutral-400">ID: {t.id.substring(0, 8)}</span>
                                </div>

                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                    <div className="flex items-start gap-3">
                                        <MapPin className="w-5 h-5 text-neutral-400 mt-0.5" />
                                        <div>
                                            <p className="text-sm font-medium text-neutral-800">Route</p>
                                            <p className="text-sm text-primary-900">{t.origin} → {t.destination}</p>
                                        </div>
                                    </div>

                                    <div className="flex items-start gap-3">
                                        <Package className="w-5 h-5 text-neutral-400 mt-0.5" />
                                        <div>
                                            <p className="text-sm font-medium text-neutral-800">Cargo</p>
                                            <p className="text-sm text-primary-900">{t.cargo_weight.toLocaleString()} kg</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="flex-shrink-0 flex gap-3">
                                {t.status === 'DRAFT' && (
                                    <button onClick={() => handleUpdateStatus(t.id, 'DISPATCHED')} className="px-4 py-2 border border-secondary-500 text-secondary-500 hover:bg-secondary-500/10 rounded-lg text-sm font-medium transition-colors">
                                        Dispatch
                                    </button>
                                )}
                                {t.status === 'DISPATCHED' && (
                                    <button onClick={() => handleUpdateStatus(t.id, 'COMPLETED')} className="flex items-center gap-2 px-4 py-2 bg-success-600 hover:bg-success-600/90 text-white rounded-lg text-sm font-medium transition-colors">
                                        <CheckCircle className="w-4 h-4" />
                                        Complete Trip
                                    </button>
                                )}
                                {(t.status === 'DRAFT' || t.status === 'DISPATCHED') && (
                                    <button onClick={() => handleUpdateStatus(t.id, 'CANCELLED')} className="px-4 py-2 border border-danger-700 text-danger-700 hover:bg-danger-700/10 rounded-lg text-sm font-medium transition-colors">
                                        Cancel
                                    </button>
                                )}
                            </div>
                        </div>
                    ))
                )}
            </div>

            {isModalOpen && (
                <div className="fixed inset-0 bg-primary-900/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl p-6 w-full max-w-2xl">
                        <h3 className="text-lg font-bold text-primary-900 mb-4">Create & Dispatch New Trip</h3>
                        <form onSubmit={handleCreate} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800 mb-1">Select Vehicle</label>
                                    <select required className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2 bg-white" value={formData.vehicle_id} onChange={e => setFormData({ ...formData, vehicle_id: e.target.value })}>
                                        <option value="">-- Choose an Available Vehicle --</option>
                                        {vehicles.filter(v => v.status === 'Available').map(v => (
                                            <option key={v.id} value={v.id}>{v.license_plate} - {v.make} {v.model} (Max: {v.max_capacity_kg}kg)</option>
                                        ))}
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800 mb-1">Select Driver</label>
                                    <select required className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2 bg-white" value={formData.driver_id} onChange={e => setFormData({ ...formData, driver_id: e.target.value })}>
                                        <option value="">-- Choose an On-Duty Driver --</option>
                                        {drivers.filter(d => d.status === 'On Duty').map(d => (
                                            <option key={d.id} value={d.id}>{d.name} ({d.license_number})</option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800 mb-1">Start Location</label>
                                    <input required type="text" className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.origin} onChange={e => setFormData({ ...formData, origin: e.target.value })} />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-neutral-800 mb-1">Destination</label>
                                    <input required type="text" className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.destination} onChange={e => setFormData({ ...formData, destination: e.target.value })} />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-800 mb-1">Cargo Weight (kg)</label>
                                <input required type="number" min="1" className="block w-full border border-neutral-400/30 rounded-md shadow-sm p-2" value={formData.cargo_weight || ''} onChange={e => setFormData({ ...formData, cargo_weight: parseInt(e.target.value) })} />
                                <p className="text-xs text-neutral-400 mt-1">Must not exceed the vehicle's maximum capacity.</p>
                            </div>

                            <div className="pt-4 flex justify-end gap-3 border-t border-neutral-400/20">
                                <button type="button" onClick={() => setIsModalOpen(false)} className="px-4 py-2 text-sm font-medium text-neutral-800 bg-neutral-50 hover:bg-neutral-400/10 rounded-lg transition-colors">Cancel</button>
                                <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-primary-900 hover:bg-primary-900/90 rounded-lg flex items-center gap-2 transition-colors">
                                    <Navigation className="w-4 h-4" />
                                    Dispatch Trip
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Trips;
