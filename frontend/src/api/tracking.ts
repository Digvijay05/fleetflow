import apiClient from './client';

export interface TrackingStatus {
    tracking_id: string;
    status: string;
    origin: string;
    destination: string;
    vehicle_plate: string;
    driver_name: string;
    cargo_weight: number;
    distance_km: number | null;
    start_time: string | null;
    end_time: string | null;
}

export interface ShipmentSummary {
    tracking_id: string;
    origin: string;
    destination: string;
    status: string;
    start_time: string | null;
}

export const getTrackingStatus = async (trackingId: string): Promise<TrackingStatus> => {
    const response = await apiClient.get<TrackingStatus>(`/tracking/${trackingId}`);
    return response.data;
};

export const getMyShipments = async (): Promise<ShipmentSummary[]> => {
    const response = await apiClient.get<ShipmentSummary[]>('/tracking/my-shipments');
    return response.data;
};
