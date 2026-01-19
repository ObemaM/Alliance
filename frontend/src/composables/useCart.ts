import { ref, computed } from 'vue';

interface Product {
  id: number;
  name: string;
  price: number;
  images?: { url: string }[];
}

interface CartItem {
  product: Product;
  quantity: number;
}

const cart = ref<CartItem[]>([]);

export function useCart() {
  function loadCart() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      cart.value = JSON.parse(savedCart);
    }
  }

  function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart.value));
  }

  function addToCart(product: Product) {
    const existingItem = cart.value.find(item => item.product.id === product.id);
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cart.value.push({ product, quantity: 1 });
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

  const cartCount = computed(() => {
    return cart.value.reduce((total, item) => total + item.quantity, 0);
  });

  const cartTotal = computed(() => {
    return cart.value.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
  });

  return {
    cart,
    cartCount,
    cartTotal,
    loadCart,
    addToCart,
    removeFromCart,
    updateQuantity,
  };
}
