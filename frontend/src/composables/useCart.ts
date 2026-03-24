import { ref, computed } from 'vue';

interface Product {
  id: number;
  name: string;
  price: number;
  
  // Объект с одним свойством url
  images?: { url: string }[];
}

interface CartItem {
  product: Product;
  quantity: number;
}

const cart = ref<CartItem[]>([]);

function loadCart() {
  const savedCart = localStorage.getItem('cart');

  if (savedCart) {
    cart.value = JSON.parse(savedCart);
  } 
}

function saveCart() {
  // stringify - переводит данные в JSON строку
  localStorage.setItem('cart', JSON.stringify(cart.value));
}

// reduce - схлопывает весь массив в одно значение

// Экспорт функция доступна и в других классах, можно сказать useCart типо класса
export function useCart() {
  const cartCount = computed(() => {
    // 0 - начальное значение
    return cart.value.reduce((total, item) => total + item.quantity, 0);
  });

  const cartTotal = computed(() => {
    return cart.value.reduce((sum, item) => sum + item.quantity * item.product.price, 0);
  });

  function addToCart(product: Product, quantity = 1) {
    const existingValue = cart.value.find(item => item.product.id === product.id);
    const normalizedQuantity = Math.max(1, quantity);
    
    if (!existingValue) {
      cart.value.push({product, quantity: normalizedQuantity});
    }
    else {
      existingValue.quantity += normalizedQuantity;
    }

    saveCart();
  }

  function removeFromCart(productId: number) {
    cart.value = cart.value.filter(item => item.product.id !== productId);
    saveCart();
  }

  function updateQuantity(productId: number, quantity: number) {
    const item = cart.value.find(item => item.product.id === productId);
    if (item) {
      if (quantity <= 0) {
        removeFromCart(productId);
      } else {
        item.quantity = quantity;
        saveCart();
      }
    }
  }

  function clearCart() {
    cart.value = [];
    saveCart();
  }
   
  return {
    cart,
    addToCart, 
    loadCart, 
    cartCount, 
    cartTotal,
    removeFromCart,
    updateQuantity,
    clearCart
  };

}
