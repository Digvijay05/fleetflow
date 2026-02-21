import { useState, useEffect } from 'react';
import { getTrackingStatus, getMyShipments, TrackingStatus, ShipmentSummary } from '../api/tracking';
import { formatDateTimeIN } from '../utils/formatters';
import { Search, Package, MapPin, Truck, User } from 'lucide-react';

const statusSteps = ['Draft', 'Dispatched', 'In Transit', 'Out for Delivery', 'Delivered'];

/**
 * Maps backend trip status to the correct step index.
 * 'Completed' is treated as fully delivered (all steps filled).
 */
const getStepIndex = (status: string): number => {
    if (status === 'Completed') return statusSteps.length - 1; // treat as fully delivered
    return statusSteps.indexOf(status);
};

const TrackingPage: React.FC = () => {
    const [trackingId, setTrackingId] = useState('');
    const [tracking, setTracking] = useState<TrackingStatus | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [myShipments, setMyShipments] = useState<ShipmentSummary[]>([]);
    const [shipmentsLoading, setShipmentsLoading] = useState(true);

    const role = localStorage.getItem('role');

    useEffect(() => {
        const fetchShipments = async () => {
            try {
                const data = await getMyShipments();
                setMyShipments(data);
            } catch {
                // Non-customer roles may get 403 — silently ignore
            } finally {
                setShipmentsLoading(false);
            }
        };
        fetchShipments();
    }, []);

    const handleSearch = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!trackingId.trim()) return;
        setLoading(true);
        setError('');
        setTracking(null);
        try {
            const data = await getTrackingStatus(trackingId.trim());
            setTracking(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Tracking ID not found.');
        } finally {
            setLoading(false);
        }
    };

    const handleRowClick = (id: string) => {
        setTrackingId(id);
        setTracking(null);
        setError('');
        // Auto-search after setting the ID
        setTimeout(async () => {
            setLoading(true);
            try {
                const data = await getTrackingStatus(id);
                setTracking(data);
            } catch (err: any) {
                setError(err.response?.data?.detail || 'Tracking ID not found.');
            } finally {
                setLoading(false);
            }
        }, 0);
    };

    const currentStepIndex = tracking ? getStepIndex(tracking.status) : -1;

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <div className="text-center">
                <Package className="w-12 h-12 text-secondary-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-primary-900">Track Your Shipment</h2>
                <p className="text-sm text-neutral-400 mt-1">Enter your tracking ID to see the current status</p>
            </div>

            {/* My Shipments Table (shown for all authenticated users who have shipments) */}
            {!shipmentsLoading && myShipments.length > 0 && (
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 overflow-hidden">
                    <div className="px-6 py-4 border-b border-neutral-400/20">
                        <h3 className="text-sm font-bold text-primary-900 uppercase tracking-wide">
                            {role === 'Customer' ? 'My Shipments' : 'Customer Shipments'}
                        </h3>
                    </div>
                    <div className="divide-y divide-neutral-400/10">
                        {myShipments.map((s) => (
                            <button
                                key={s.tracking_id}
                                onClick={() => handleRowClick(s.tracking_id)}
                                className={`w-full flex items-center justify-between px-6 py-3 text-left hover:bg-neutral-50 transition-colors ${trackingId === s.tracking_id ? 'bg-secondary-500/5' : ''}`}
                            >
                                <div className="flex items-center gap-3 min-w-0">
                                    <span className="text-xs font-mono bg-secondary-500/10 text-secondary-500 px-1.5 py-0.5 rounded flex-shrink-0">{s.tracking_id}</span>
                                    <span className="text-sm text-primary-900 truncate">{s.origin} → {s.destination}</span>
                                </div>
                                <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0 ${s.status === 'Completed' || s.status === 'Delivered' ? 'bg-success-600/10 text-success-600' :
                                    s.status === 'Cancelled' ? 'bg-danger-700/10 text-danger-700' :
                                        'bg-warning-500/10 text-warning-500'
                                    }`}>{s.status}</span>
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Search */}
            <form onSubmit={handleSearch} className="flex gap-3">
                <input
                    type="text"
                    value={trackingId}
                    onChange={(e) => setTrackingId(e.target.value)}
                    placeholder="e.g. TRK-A1B2C3D4"
                    className="flex-1 px-4 py-3 border border-neutral-400/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-secondary-500"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className="px-6 py-3 bg-secondary-500 hover:bg-secondary-500/90 text-white rounded-lg text-sm font-medium flex items-center gap-2 transition-colors disabled:opacity-50"
                >
                    <Search className="w-4 h-4" />
                    {loading ? 'Searching...' : 'Track'}
                </button>
            </form>

            {error && (
                <div className="bg-danger-700/10 border border-danger-700/30 text-danger-700 px-4 py-3 rounded-lg text-sm">
                    {error}
                </div>
            )}

            {tracking && (
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6 space-y-6">
                    {/* Header */}
                    <div className="flex items-center justify-between border-b border-neutral-400/20 pb-4">
                        <div>
                            <span className="text-xs font-mono bg-secondary-500/10 text-secondary-500 px-2 py-1 rounded">{tracking.tracking_id}</span>
                            <h3 className="text-lg font-bold text-primary-900 mt-2">{tracking.origin} → {tracking.destination}</h3>
                        </div>
                        <span className={`text-sm font-medium px-3 py-1 rounded-full ${tracking.status === 'Delivered' || tracking.status === 'Completed' ? 'bg-success-600/10 text-success-600' :
                            tracking.status === 'Cancelled' ? 'bg-danger-700/10 text-danger-700' :
                                'bg-warning-500/10 text-warning-500'
                            }`}>{tracking.status}</span>
                    </div>

                    {/* Details */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div className="flex items-center gap-2 text-neutral-400">
                            <Truck className="w-4 h-4" />
                            <span>Vehicle: <span className="text-primary-900 font-medium">{tracking.vehicle_plate}</span></span>
                        </div>
                        <div className="flex items-center gap-2 text-neutral-400">
                            <User className="w-4 h-4" />
                            <span>Driver: <span className="text-primary-900 font-medium">{tracking.driver_name}</span></span>
                        </div>
                        <div className="flex items-center gap-2 text-neutral-400">
                            <Package className="w-4 h-4" />
                            <span>Cargo: <span className="text-primary-900 font-medium">{tracking.cargo_weight} kg</span></span>
                        </div>
                        <div className="flex items-center gap-2 text-neutral-400">
                            <MapPin className="w-4 h-4" />
                            <span>Distance: <span className="text-primary-900 font-medium">{tracking.distance_km ? `${tracking.distance_km} km` : '—'}</span></span>
                        </div>
                    </div>

                    {/* Timeline */}
                    <div>
                        <h4 className="text-sm font-bold text-primary-900 mb-4 uppercase tracking-wide">Shipment Timeline</h4>
                        <div className="space-y-0">
                            {statusSteps.map((step, idx) => {
                                const isCompleted = idx <= currentStepIndex;
                                const isCurrent = idx === currentStepIndex;
                                return (
                                    <div key={step} className="flex items-start gap-4">
                                        <div className="flex flex-col items-center">
                                            <div className={`w-4 h-4 rounded-full border-2 ${isCompleted ? 'bg-secondary-500 border-secondary-500' : 'bg-white border-neutral-400/40'
                                                } ${isCurrent ? 'ring-4 ring-secondary-500/20' : ''}`} />
                                            {idx < statusSteps.length - 1 && (
                                                <div className={`w-0.5 h-8 ${isCompleted ? 'bg-secondary-500' : 'bg-neutral-400/20'}`} />
                                            )}
                                        </div>
                                        <div className={`pb-6 ${isCompleted ? 'text-primary-900' : 'text-neutral-400/60'}`}>
                                            <p className={`text-sm font-medium ${isCurrent ? 'text-secondary-500' : ''}`}>
                                                {step}
                                                {isCurrent && <span className="ml-2 text-xs bg-secondary-500/10 text-secondary-500 px-2 py-0.5 rounded">Current</span>}
                                            </p>
                                            {isCurrent && tracking.start_time && (
                                                <p className="text-xs text-neutral-400 mt-1">{formatDateTimeIN(tracking.start_time)}</p>
                                            )}
                                            {step === 'Delivered' && tracking.end_time && isCompleted && (
                                                <p className="text-xs text-neutral-400 mt-1">{formatDateTimeIN(tracking.end_time)}</p>
                                            )}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TrackingPage;
