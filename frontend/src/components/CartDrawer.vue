<template>
  <div v-if="isOpen" class="cart-drawer-overlay" @click="close">
    <div class="cart-drawer" @click.stop>
      <div class="cart-drawer__header">
        <h2 class="cart-drawer__title">Корзина</h2>
        <button class="cart-drawer__close" @click="close">
          <Icon name="X" :size="24" />
        </button>
      </div>

      <div class="cart-drawer__content">
        <div v-if="items.length === 0" class="cart-drawer__empty">
          <p class="cart-drawer__empty-text">Корзина пуста</p>
          <p class="cart-drawer__empty-subtext">Добавьте товары из каталога</p>
        </div>
        <div v-else class="cart-drawer__items">
          <div v-for="item in items" :key="item.product.id" class="cart-item">
            <img
              v-if="item.product.images && item.product.images.length > 0"
              :src="`${API_BASE_URL}${item.product.images[0]?.url}`"
              :alt="item.product.name"
              class="cart-item__image"
            />
            <div class="cart-item__info">
              <h4 class="cart-item__name">{{ item.product.name }}</h4>
              <p class="cart-item__price">{{ item.product.price }} ₽</p>
              <div class="cart-item__controls">
                <button
                  class="cart-item__btn"
                  @click="updateQuantity(item.product.id, item.quantity - 1)"
                >
                  -
                </button>
                <span class="cart-item__quantity">{{ item.quantity }}</span>
                <button
                  class="cart-item__btn"
                  @click="updateQuantity(item.product.id, item.quantity + 1)"
                >
                  +
                </button>
                <button class="cart-item__remove" @click="removeItem(item.product.id)">
                  <Icon name="Trash2" :size="20" />
                </button>
              </div>
            </div>
          </div>
          <button class="cart-drawer__clear" @click="openClearDialog">
            Очистить корзину
          </button>
        </div>
      </div>

      <div v-if="items.length > 0" class="cart-drawer__footer">
        <div class="cart-drawer__total">
          <span class="cart-drawer__total-label">Итого:</span>
          <span class="cart-drawer__total-value">{{ total.toFixed(2) }} ₽</span>
        </div>
        <button class="cart-drawer__checkout" @click="handleCheckout">
          Оформить заказ
        </button>
      </div>
    </div>
  </div>
  <!-- Диалог подтверждения очистки корзины -->
  <div v-if="showClearCartButton" class="dialog-overlay" @click="cancelClearDialog">
    <div class="dialog" @click.stop>
      <h3>Подтверждение</h3>
      <p>Вы действительно хотите очистить корзину?</p>
      <div class="dialog-buttons">
        <button class="dialog-btn dialog-btn--cancel" @click="cancelClearDialog">
          Отмена
        </button>
        <button class="dialog-btn dialog-btn--confirm" @click="confirmClearDialog">
          Очистить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import Icon from './Icon.vue';

interface CartItem {
  product: {
    id: number;
    name: string;
    price: number;
    images?: { url: string }[];
  };
  quantity: number;
}

interface Props {
  isOpen: boolean;
  items: CartItem[];
}

interface Emits {
  (e: 'close'): void;
  (e: 'updateQuantity', productId: number, quantity: number): void;
  (e: 'removeItem', productId: number): void;
  (e: 'checkout'): void;
  (e: 'clearCart'): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const showClearCartButton = ref(false);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const total = computed(() => {
  return props.items.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
});

function close() {
  emit('close');
}

function updateQuantity(productId: number, quantity: number) {
  emit('updateQuantity', productId, quantity);
}

function removeItem(productId: number) {
  emit('removeItem', productId);
}

function handleCheckout() {
  emit('checkout');
}

function handleClearCart() {
  emit('clearCart');
}

function openClearDialog() {
  showClearCartButton.value = true;
}

function confirmClearDialog() {
  handleClearCart();
  showClearCartButton.value = false;
}

function cancelClearDialog() {
  showClearCartButton.value = false;
}



</script>

<style scoped>
.cart-drawer-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  padding: 20px;
}

.cart-drawer {
  position: relative;
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  background: white;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  animation: fadeIn 0.3s ease-out;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.cart-drawer__header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f5f6f7;
  border-radius: 12px 12px 0 0;
}

.cart-drawer__title {
  font-size: 22px;
  font-weight: 600;
  color: #1e1e1e;
  margin: 0;
}

.cart-drawer__close {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
  color: #1e1e1e;
}

.cart-drawer__close:hover {
  background: #e5e7eb;
}

.cart-drawer__content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.cart-drawer__note {
  font-size: 13px;
  color: #9ca3af;
  text-align: center;
  margin: 10px 0 0 0;
}

.cart-drawer__empty {
  align-items: center;
  text-align: center;
  margin: 20px 0;
  color: #6b7280;
}

.cart-drawer__empty-text {
  font-size: 18px;
  margin: 0 0 8px 0;
  color: #1e1e1e;
}

.cart-drawer__empty-subtext {
  font-size: 14px;
  margin: 0;
}

.cart-drawer__items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item {
  display: flex;
  gap: 16px;
  background: #fafafa;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.cart-item__image {
  width: 80px;
  height: 80px;
  object-fit: contain;
  border-radius: 8px;
  background: white;
  flex-shrink: 0;
  border: 1px solid #e5e7eb;
}

.cart-item__info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.cart-item__name {
  font-size: 15px;
  font-weight: 500;
  color: #1e1e1e;
  margin: 0 0 6px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.cart-item__price {
  font-size: 18px;
  font-weight: 700;
  color: #1e1e1e;
  margin: 0 0 10px 0;
}

.cart-item__controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.cart-item__btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  color: #1e1e1e;
  transition: all 0.2s ease;
}

.cart-item__btn:hover:not(:disabled) {
  background: #f5f6f7;
  border-color: #d1d5db;
}

.cart-item__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.cart-item__quantity {
  font-size: 15px;
  font-weight: 600;
  color: #1e1e1e;
  min-width: 24px;
  text-align: center;
}

.cart-item__remove {
  background: none;
  border-radius: 12px;
  border: none;
  padding: 6px;
  cursor: pointer;
  color: #bd0707;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
  margin-left: auto;
}

.cart-item__remove:hover {
  background: #e5e7eb;
}

.cart-drawer__footer {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: #f5f6f7;
  border-radius: 0 0 12px 12px;
}

.cart-drawer__total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.cart-drawer__total-label {
  font-size: 16px;
  color: #6b7280;
}

.cart-drawer__total-value {
  font-size: 26px;
  font-weight: 700;
  color: #1e1e1e;
}

.cart-drawer__checkout {
  width: 100%;
  background: #1e1e1e;
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.cart-drawer__checkout:hover {
  background: #374151;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.cart-drawer__clear {
  width: 35%;
  background: white;
  color: #1e1e1e;
  border: 1px solid #1e1e1e;
  padding: 10px 10px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
}

.cart-drawer__clear:hover {
  background: #1e1e1e;
  color: white;
}

.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.dialog {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 90%;
}

.dialog h3 {
  margin: 0 0 16px 0;
  color: #1e1e1e;
}

.dialog p {
  margin: 0 0 24px 0;
  color: #6b7280;
}

.dialog-buttons {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.dialog-btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dialog-btn--cancel {
  background: #f5f6f7;
  color: #1e1e1e;
}

.dialog-btn--cancel:hover {
  background: #e5e7eb;
}

.dialog-btn--confirm {
  background: #bd0707;
  color: white;
}

.dialog-btn--confirm:hover {
  background: #9a0606;
}
</style>
