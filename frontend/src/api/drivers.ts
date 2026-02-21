import apiClient from './client';

export interface Driver {
    id: string;
    name: string;
    license_number: string;
    license_expiry: string;
    safety_score: number | null;
    status: 'Off Duty' | 'On Duty' | 'On Trip' | 'Suspended';
}

export interface DriverCreate {
    name: string;
    license_number: string;
    license_expiry: string;
    safety_score?: number;
}

export interface DriverUpdate {
    name?: string;
    status?: string;
    license_expiry?: string;
    safety_score?: number;
}

export const getDrivers = async (): Promise<Driver[]> => {
    const response = await apiClient.get<Driver[]>('/drivers/');
    return response.data;
};

export const createDriver = async (data: DriverCreate): Promise<Driver> => {
    const response = await apiClient.post<Driver>('/drivers/', data);
    return response.data;
};

export const updateDriver = async (id: string, data: DriverUpdate): Promise<Driver> => {
    const response = await apiClient.patch<Driver>(`/drivers/${id}`, data);
    return response.data;
};
