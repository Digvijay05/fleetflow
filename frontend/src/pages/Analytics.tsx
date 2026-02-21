import React, { useEffect, useState } from 'react';
import { getROIMetrics, ROIMetrics, getActiveTrips, ActiveTrip } from '../api/analytics';
import { formatINR, formatDateTimeIN } from '../utils/formatters';
import { IndianRupee, TrendingUp, Fuel, Wrench, ArrowRight } from 'lucide-react';

const Analytics: React.FC = () => {
    const [roi, setRoi] = useState<ROIMetrics | null>(null);
    const [activeTrips, setActiveTrips] = useState<ActiveTrip[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [roiData, tripsData] = await Promise.all([
                    getROIMetrics(),
                    getActiveTrips(),
                ]);
                setRoi(roiData);
                setActiveTrips(tripsData);
            } catch (err: any) {
                setError('Failed to load analytics data.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex h-64 items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-secondary-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-danger-700/10 border border-danger-700/30 text-danger-700 px-4 py-3 rounded-lg text-sm">
                {error}
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <h2 className="text-xl font-bold text-primary-900">Financial Analytics</h2>

            {/* Financial KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="Total Revenue"
                    value={formatINR(roi?.totalRevenue || 0)}
                    icon={<IndianRupee className="w-6 h-6 text-white" />}
                    colorClass="bg-success-600"
                />
                <KPICard
                    title="Total Expenses"
                    value={formatINR(roi?.totalExpenses || 0)}
                    icon={<Fuel className="w-6 h-6 text-white" />}
                    colorClass="bg-danger-700"
                />
                <KPICard
                    title="Net Profit"
                    value={formatINR(roi?.netProfit || 0)}
                    icon={<TrendingUp className="w-6 h-6 text-white" />}
                    colorClass={roi && roi.netProfit >= 0 ? 'bg-success-600' : 'bg-danger-700'}
                />
                <KPICard
                    title="ROI"
                    value={`${roi?.roiPercentage?.toFixed(1) || 0}%`}
                    icon={<TrendingUp className="w-6 h-6 text-white" />}
                    colorClass="bg-secondary-500"
                />
            </div>

            {/* Efficiency Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6">
                    <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-wide">Cost per Km</h3>
                    <p className="text-3xl font-bold text-primary-900 mt-2">{formatINR(roi?.costPerKm || 0)}</p>
                    <p className="text-sm text-neutral-400 mt-1">Per kilometre operating cost</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6">
                    <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-wide">Fuel Efficiency</h3>
                    <p className="text-3xl font-bold text-primary-900 mt-2">{roi?.fuelEfficiencyKmPerL?.toFixed(1) || 0} km/L</p>
                    <p className="text-sm text-neutral-400 mt-1">Average fleet mileage</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6">
                    <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-wide">Fuel Cost</h3>
                    <p className="text-3xl font-bold text-primary-900 mt-2">{formatINR(roi?.totalFuelCost || 0)}</p>
                    <p className="text-sm text-neutral-400 mt-1">
                        <Wrench className="inline w-3 h-3 mr-1" />
                        Maintenance: {formatINR(roi?.totalMaintenanceCost || 0)}
                    </p>
                </div>
            </div>

            {/* Active Trips */}
            <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6">
                <h3 className="text-lg font-bold text-primary-900 mb-4">Active Trips</h3>
                {activeTrips.length === 0 ? (
                    <p className="text-sm text-neutral-400 italic">No active trips at this time.</p>
                ) : (
                    <div className="space-y-3">
                        {activeTrips.map((trip) => (
                            <div key={trip.id} className="flex items-center justify-between bg-neutral-50 rounded-lg p-4 border border-neutral-400/10">
                                <div className="flex items-center gap-4">
                                    <span className="text-xs font-mono bg-secondary-500/10 text-secondary-500 px-2 py-1 rounded">{trip.tracking_id}</span>
                                    <span className="text-sm font-medium text-primary-900">{trip.origin}</span>
                                    <ArrowRight className="w-4 h-4 text-neutral-400" />
                                    <span className="text-sm font-medium text-primary-900">{trip.destination}</span>
                                </div>
                                <div className="flex items-center gap-6">
                                    <span className="text-sm text-neutral-400">{trip.driver_name}</span>
                                    <span className="text-xs font-mono text-neutral-400">{trip.vehicle_plate}</span>
                                    <span className="text-xs font-medium bg-warning-500/10 text-warning-500 px-2 py-1 rounded">{trip.status}</span>
                                    <span className="text-xs text-neutral-400">{formatDateTimeIN(trip.start_time)}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

interface KPICardProps {
    title: string;
    value: string;
    icon: React.ReactNode;
    colorClass: string;
}

const KPICard: React.FC<KPICardProps> = ({ title, value, icon, colorClass }) => (
    <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6 flex items-start gap-4">
        <div className={`p-4 rounded-xl ${colorClass}`}>{icon}</div>
        <div>
            <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-wide">{title}</h3>
            <p className="text-2xl font-bold text-primary-900 mt-1">{value}</p>
        </div>
    </div>
);

export default Analytics;
