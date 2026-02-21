import apiClient from './client';

export interface LoginResponse {
    access_token: string;
    role: string;
}

export const login = async (email: string, password: string): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', {
        email,
        password
    });

    return response.data;
};
