import apiClient from './client';

export interface Vehicle {
    id: string;
    license_plate: string;
    make: string;
    model: string;
    year: number;
    max_capacity_kg: number;
    status: 'Available' | 'On Trip' | 'In Shop' | 'Retired';
}

export interface VehicleCreate {
    license_plate: string;
    make: string;
    model: string;
    year: number;
    max_capacity_kg: number;
}

export interface VehicleUpdate {
    max_capacity_kg?: number;
    status?: string;
}

export const getVehicles = async (): Promise<Vehicle[]> => {
    const response = await apiClient.get<Vehicle[]>('/vehicles/');
    return response.data;
};

export const createVehicle = async (data: VehicleCreate): Promise<Vehicle> => {
    const response = await apiClient.post<Vehicle>('/vehicles/', data);
    return response.data;
};

export const updateVehicle = async (id: string, data: VehicleUpdate): Promise<Vehicle> => {
    const response = await apiClient.patch<Vehicle>(`/vehicles/${id}`, data);
    return response.data;
};

export const retireVehicle = async (id: string): Promise<Vehicle> => {
    const response = await apiClient.patch<Vehicle>(`/vehicles/${id}/retire`);
    return response.data;
};
