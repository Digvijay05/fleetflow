import apiClient from './client';
export interface Trip {
    id: string;
    vehicle_id: string;
    driver_id: string;
    origin: string;
    destination: string;
    cargo_weight: number;
    distance_km?: number;
    revenue?: number;
    status: 'DRAFT' | 'DISPATCHED' | 'COMPLETED' | 'CANCELLED';
    start_time?: string;
    end_time?: string;
}

export interface TripCreate {
    vehicle_id: string;
    driver_id: string;
    origin: string;
    destination: string;
    cargo_weight: number;
}

export interface TripUpdateStatus {
    status: 'DRAFT' | 'DISPATCHED' | 'COMPLETED' | 'CANCELLED';
    odometer_km?: number;
}

export const getTrips = async (): Promise<Trip[]> => {
    const response = await apiClient.get<Trip[]>('/trips/');
    return response.data;
};

export const createTrip = async (data: TripCreate): Promise<Trip> => {
    const response = await apiClient.post<Trip>('/trips/', data);
    return response.data;
};

export const updateTripStatus = async (id: string, data: TripUpdateStatus): Promise<Trip> => {
    const response = await apiClient.patch<Trip>(`/trips/${id}/status`, data);
    return response.data;
};
