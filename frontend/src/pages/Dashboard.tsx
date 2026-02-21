import React, { useEffect, useState } from 'react';
import { getDashboardMetrics, DashboardMetrics, getROIMetrics, ROIMetrics, getActiveTrips, ActiveTrip } from '../api/analytics';
import { formatINR } from '../utils/formatters';
import { Truck, AlertTriangle, Activity, IndianRupee, ArrowRight } from 'lucide-react';

const Dashboard: React.FC = () => {
    const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
    const [roi, setRoi] = useState<ROIMetrics | null>(null);
    const [activeTrips, setActiveTrips] = useState<ActiveTrip[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchAll = async () => {
            try {
                const [metricsData, roiData, tripsData] = await Promise.all([
                    getDashboardMetrics(),
                    getROIMetrics(),
                    getActiveTrips(),
                ]);
                setMetrics(metricsData);
                setRoi(roiData);
                setActiveTrips(tripsData);
            } catch (err: any) {
                setError('Failed to load dashboard data.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchAll();
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
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                    title="Active Fleet"
                    value={metrics?.activeFleet.toString() || '0'}
                    subtitle={`Out of ${metrics?.totalFleet} total vehicles`}
                    icon={<Truck className="w-6 h-6 text-white" />}
                    colorClass="bg-secondary-500"
                />
                <MetricCard
                    title="Utilization Rate"
                    value={`${((metrics?.utilizationRate || 0) * 100).toFixed(0)}%`}
                    subtitle="Target: 85%"
                    icon={<Activity className="w-6 h-6 text-white" />}
                    colorClass="bg-primary-900"
                />
                <MetricCard
                    title="Maintenance Alerts"
                    value={metrics?.maintenanceAlerts.toString() || '0'}
                    subtitle="Vehicles currently in shop"
                    icon={<AlertTriangle className="w-6 h-6 text-white" />}
                    colorClass={metrics?.maintenanceAlerts && metrics.maintenanceAlerts > 0 ? 'bg-danger-700' : 'bg-success-600'}
                />
                <MetricCard
                    title="Financial ROI"
                    value={`${roi?.roiPercentage?.toFixed(1) || 0}%`}
                    subtitle={`Net: ${formatINR(roi?.netProfit || 0)}`}
                    icon={<IndianRupee className="w-6 h-6 text-white" />}
                    colorClass={roi && roi.netProfit >= 0 ? 'bg-success-600' : 'bg-danger-700'}
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Active Trips Feed */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-neutral-400/20">
                    <h3 className="text-lg font-bold text-primary-900 mb-4">Active Trips</h3>
                    {activeTrips.length === 0 ? (
                        <div className="h-48 bg-neutral-50 rounded-lg border border-neutral-400/20 flex items-center justify-center text-neutral-400 text-sm italic">
                            No active trips at this time
                        </div>
                    ) : (
                        <div className="space-y-3 max-h-64 overflow-y-auto">
                            {activeTrips.map((trip) => (
                                <div key={trip.id} className="flex items-center justify-between bg-neutral-50 rounded-lg p-3 border border-neutral-400/10">
                                    <div className="flex items-center gap-2 min-w-0">
                                        <span className="text-xs font-mono bg-secondary-500/10 text-secondary-500 px-1.5 py-0.5 rounded flex-shrink-0">{trip.tracking_id}</span>
                                        <span className="text-sm text-primary-900 truncate">{trip.origin}</span>
                                        <ArrowRight className="w-3 h-3 text-neutral-400 flex-shrink-0" />
                                        <span className="text-sm text-primary-900 truncate">{trip.destination}</span>
                                    </div>
                                    <div className="flex items-center gap-3 flex-shrink-0">
                                        <span className="text-xs text-neutral-400">{trip.driver_name}</span>
                                        <span className="text-xs font-mono text-neutral-400">{trip.vehicle_plate}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Revenue vs Expenses */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-neutral-400/20">
                    <h3 className="text-lg font-bold text-primary-900 mb-4">Revenue vs Expenses</h3>
                    <div className="space-y-4">
                        <div>
                            <div className="flex justify-between mb-1">
                                <span className="text-sm text-neutral-400">Revenue</span>
                                <span className="text-sm font-medium text-success-600">{formatINR(roi?.totalRevenue || 0)}</span>
                            </div>
                            <div className="w-full bg-neutral-400/10 rounded-full h-3">
                                <div className="bg-success-600 h-3 rounded-full transition-all duration-500"
                                    style={{ width: `${roi && roi.totalRevenue > 0 ? Math.min((roi.totalRevenue / (roi.totalRevenue + roi.totalExpenses)) * 100, 100) : 0}%` }} />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between mb-1">
                                <span className="text-sm text-neutral-400">Fuel Cost</span>
                                <span className="text-sm font-medium text-danger-700">{formatINR(roi?.totalFuelCost || 0)}</span>
                            </div>
                            <div className="w-full bg-neutral-400/10 rounded-full h-3">
                                <div className="bg-danger-700 h-3 rounded-full transition-all duration-500"
                                    style={{ width: `${roi && roi.totalRevenue > 0 ? Math.min((roi.totalFuelCost / roi.totalRevenue) * 100, 100) : 0}%` }} />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between mb-1">
                                <span className="text-sm text-neutral-400">Maintenance</span>
                                <span className="text-sm font-medium text-warning-500">{formatINR(roi?.totalMaintenanceCost || 0)}</span>
                            </div>
                            <div className="w-full bg-neutral-400/10 rounded-full h-3">
                                <div className="bg-warning-500 h-3 rounded-full transition-all duration-500"
                                    style={{ width: `${roi && roi.totalRevenue > 0 ? Math.min((roi.totalMaintenanceCost / roi.totalRevenue) * 100, 100) : 0}%` }} />
                            </div>
                        </div>
                        <div className="pt-3 border-t border-neutral-400/20 flex justify-between">
                            <span className="text-sm font-medium text-primary-900">Cost per Km</span>
                            <span className="text-sm font-bold text-primary-900">{formatINR(roi?.costPerKm || 0)}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-sm font-medium text-primary-900">Fuel Efficiency</span>
                            <span className="text-sm font-bold text-primary-900">{roi?.fuelEfficiencyKmPerL?.toFixed(1) || 0} km/L</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

interface MetricCardProps {
    title: string;
    value: string;
    subtitle: string;
    icon: React.ReactNode;
    colorClass: string;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtitle, icon, colorClass }) => (
    <div className="bg-white rounded-xl shadow-sm border border-neutral-400/20 p-6 flex items-start gap-4">
        <div className={`p-4 rounded-xl ${colorClass}`}>
            {icon}
        </div>
        <div>
            <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-wide">{title}</h3>
            <p className="text-2xl font-bold text-primary-900 mt-1">{value}</p>
            <p className="text-sm text-neutral-400 mt-1">{subtitle}</p>
        </div>
    </div>
);

export default Dashboard;
