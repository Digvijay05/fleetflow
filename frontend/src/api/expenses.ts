import apiClient from './client';

export interface Expense {
    id: string;
    vehicle_id: string;
    trip_id: string;
    fuel_liters: number;
    fuel_cost: number;
    date: string;
}

export interface ExpenseCreate {
    vehicle_id: string;
    trip_id: string;
    fuel_liters: number;
    fuel_cost: number;
    date: string;
}

export const getExpenses = async (): Promise<Expense[]> => {
    const response = await apiClient.get<Expense[]>('/expenses/');
    return response.data;
};

export const createExpense = async (data: ExpenseCreate): Promise<Expense> => {
    const response = await apiClient.post<Expense>('/expenses/', data);
    return response.data;
};
