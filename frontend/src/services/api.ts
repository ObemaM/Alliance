import axios from 'axios';
import type { Country, Color, Category } from '../types';

// Базовый URL твоего FastAPI бэкенда
const API_BASE_URL = 'http://localhost:8000';

// Создаем экземпляр axios с базовым URL
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Функция для получения всех стран
export const getCountries = async (): Promise<Country[]> => {
  const response = await api.get<Country[]>('/countries/');
  return response.data;
};

// Функция для создания новой страны
export const createCountry = async (name: string): Promise<Country> => {
  const response = await api.post<Country>('/countries/', { name });
  return response.data;
};

// Функция для получения всех цветов
export const getColors = async (): Promise<Color[]> => {
  const response = await api.get<Color[]>('/colors/');
  return response.data;
};

export const getCategories = async (): Promise<Category[]> => {
  const response = await api.get<Category[]>('/categories/');
  return response.data;
};