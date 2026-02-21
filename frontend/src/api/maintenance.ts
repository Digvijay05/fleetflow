import apiClient from './client';

export interface MaintenanceLog {
    id: string;
    vehicle_id: string;
    type: 'Oil Change' | 'Tire Replacement' | 'Engine Repair' | 'Inspection' | 'Other';
    description: string;
    cost: number;
    status: 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED';
    date: string;
}

export interface MaintenanceLogCreate {
    vehicle_id: string;
    type: 'Oil Change' | 'Tire Replacement' | 'Engine Repair' | 'Inspection' | 'Other';
    description: string;
    cost: number;
    date: string;
}

export interface MaintenanceLogUpdate {
    status: 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED';
    cost?: number;
}

export const getMaintenanceLogs = async (): Promise<MaintenanceLog[]> => {
    const response = await apiClient.get<MaintenanceLog[]>('/maintenance/');
    return response.data;
};

export const getMaintenanceLog = async (id: string): Promise<MaintenanceLog> => {
    const response = await apiClient.get<MaintenanceLog>(`/maintenance/${id}`);
    return response.data;
};

export const createMaintenanceLog = async (data: MaintenanceLogCreate): Promise<MaintenanceLog> => {
    const response = await apiClient.post<MaintenanceLog>('/maintenance/', data);
    return response.data;
};

export const updateMaintenanceLogStatus = async (id: string, data: MaintenanceLogUpdate): Promise<MaintenanceLog> => {
    const response = await apiClient.patch<MaintenanceLog>(`/maintenance/${id}`, data);
    return response.data;
};
