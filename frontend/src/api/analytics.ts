import apiClient from './client';

export interface DashboardMetrics {
    activeFleet: number;
    maintenanceAlerts: number;
    utilizationRate: number;
    totalFleet: number;
}

export interface ROIMetrics {
    currency: string;
    totalRevenue: number;
    totalFuelCost: number;
    totalMaintenanceCost: number;
    totalExpenses: number;
    netProfit: number;
    roiPercentage: number;
    costPerKm: number;
    fuelEfficiencyKmPerL: number;
}

export interface ActiveTrip {
    id: string;
    tracking_id: string;
    origin: string;
    destination: string;
    status: string;
    vehicle_plate: string;
    driver_name: string;
    cargo_weight: number;
    start_time: string | null;
}

export const getDashboardMetrics = async (): Promise<DashboardMetrics> => {
    const response = await apiClient.get<DashboardMetrics>('/analytics/dashboard');
    return response.data;
};

export const getROIMetrics = async (): Promise<ROIMetrics> => {
    const response = await apiClient.get<ROIMetrics>('/analytics/roi');
    return response.data;
};

export const getActiveTrips = async (): Promise<ActiveTrip[]> => {
    const response = await apiClient.get<ActiveTrip[]>('/analytics/active-trips');
    return response.data;
};
