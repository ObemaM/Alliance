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

export interface Category {
  id: number;
  name: string;
  slug: string;
  parent_id: number | null;
}