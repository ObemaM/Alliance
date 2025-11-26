// Типы для данных из базы

// export - делает интерфейс доступным в других файлах
export interface Country {
  id: number;
  name: string;
}

export interface Color {
  id: number;
  name: string;
  code: string | null;
}