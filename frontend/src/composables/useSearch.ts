import { ref, watch, type Ref } from 'vue';

interface Product {
    id: number;
    name: string;
    description?: string;
    price: number;
    images?: { url: string }[];
}

function debounce<T extends (...args: any[]) => any>(
    func: T,
    wait: number
): (...args: Parameters<T>) => void {
    let timeout: ReturnType<typeof setTimeout> | null = null;

    return function (this: any, ...args: Parameters<T>) {
        if (timeout) clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

export function useSearch(searchTerm: Ref<string>) {
    const searchResults = ref<Product[]>([]);
    const isLoading = ref(false)

    async function performSearch(query: string) {
        if (!query.trim()) {
            searchResults.value = [];
            return;
        }
        isLoading.value = true;

        try {
            const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
            const response = await fetch(`${API_BASE_URL}/products/?q=${query}`);

            if (!response.ok) throw new Error('Ошибка поиска');

            searchResults.value = await response.json();
        } catch (error) {
            console.error('Ошибка поиска:', error);
            searchResults.value = [];
        } finally {
            isLoading.value = false;
        }
    }

    const debouncedSearch = debounce(performSearch, 300);
    watch(searchTerm, (newVal) => {
        debouncedSearch(newVal);
    });

    return {searchResults, isLoading};
}


