<script setup lang="ts">
import { computed, shallowRef, watch } from 'vue'

import Modal from '../Modal.vue'
import { useCart } from '../../composables/useCart'
import type { Product, ProductAttribute, ProductImage } from '../../types/product'

interface ProductMetaItem {
    label: string
    value: string
    tone?: 'default' | 'color'
    colorCode?: string | null
}

interface ProductAttributeItem {
    name: string
    value: string
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const props = defineProps<{
    modelValue: boolean
    product?: Product
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
}>()

const { addToCart } = useCart()
type CartProduct = Parameters<typeof addToCart>[0]

const currentImageIndex = shallowRef(0)
const quantity = shallowRef(1)

const buttonText = 'Добавить в корзину'

const isOpen = computed({
    get: () => props.modelValue,
    set: (value: boolean) => emit('update:modelValue', value),
})

const resolvedImages = computed<ProductImage[]>(() => {
    return props.product?.images?.filter((image) => Boolean(image.url)) ?? []
})

const totalImages = computed(() => resolvedImages.value.length)
const hasImages = computed(() => totalImages.value > 0)
const hasMultipleImages = computed(() => totalImages.value > 1)

const currentImage = computed<ProductImage | null>(() => {
    if (!hasImages.value) {
        return null
    }

    return resolvedImages.value[currentImageIndex.value] ?? resolvedImages.value[0] ?? null
})

const currentImageUrl = computed(() => {
    const imageUrl = currentImage.value?.url
    if (!imageUrl) {
        return null
    }

    return imageUrl.startsWith('http') ? imageUrl : `${API_BASE_URL}${imageUrl}`
})

const resolvedCategoryName = computed(() => props.product?.category?.name ?? null)
const resolvedMaterialName = computed(() => props.product?.material?.name ?? null)
const resolvedCountryName = computed(() => props.product?.country?.name ?? null)
const resolvedColorName = computed(() => props.product?.color?.name ?? null)
const resolvedColorCode = computed(() => props.product?.color?.code ?? null)

const availability = computed(() => {
    const stock = props.product?.quantity

    if (typeof stock !== 'number') {
        return {
            label: 'Под заказ',
            className: 'product-stock--order',
        }
    }

    if (stock > 0) {
        return {
            label: 'В наличии',
            className: 'product-stock--available',
        }
    }

    return {
        label: 'Нет в наличии',
        className: 'product-stock--unavailable',
    }
})

const maxQuantity = computed(() => {
    const stock = props.product?.quantity
    return typeof stock === 'number' && stock > 0 ? stock : 999
})

const productMetaItems = computed<ProductMetaItem[]>(() => {
    const items: ProductMetaItem[] = []

    if (resolvedCategoryName.value) {
        items.push({ label: 'Категория', value: resolvedCategoryName.value })
    }

    if (resolvedMaterialName.value) {
        items.push({ label: 'Материал', value: resolvedMaterialName.value })
    }

    if (resolvedColorName.value) {
        items.push({
            label: 'Цвет',
            value: resolvedColorName.value,
            tone: 'color',
            colorCode: resolvedColorCode.value,
        })
    }

    if (resolvedCountryName.value) {
        items.push({ label: 'Страна', value: resolvedCountryName.value })
    }

    if (props.product?.purpose) {
        items.push({ label: 'Назначение', value: props.product.purpose })
    }

    if (props.product?.weight) {
        items.push({ label: 'Вес', value: props.product.weight })
    }

    if (typeof props.product?.pack_quantity === 'number') {
        items.push({ label: 'В упаковке', value: `${props.product.pack_quantity} шт.` })
    }

    return items
})

const attributeItems = computed<ProductAttributeItem[]>(() => {
    return (
        props.product?.product_attributes
            ?.map((attribute: ProductAttribute) => {
                const name = attribute.attribute?.name?.trim()
                const value = (attribute.value_text ?? '').trim()

                if (!name || !value) {
                    return null
                }

                return { name, value }
            })
            .filter((attribute): attribute is ProductAttributeItem => attribute !== null) ?? []
    )
})

const formattedPrice = computed(() => formatPrice(props.product?.price))

watch(
    () => props.product?.id,
    () => {
        resetModalState()
    },
    { immediate: true },
)

watch(
    () => props.modelValue,
    (isVisible) => {
        if (isVisible) {
            resetModalState()
        }
    },
)

watch(maxQuantity, (value) => {
    quantity.value = clampQuantity(quantity.value, value)
})

function formatPrice(price: number | null | undefined) {
    if (typeof price !== 'number') {
        return 'Цена по запросу'
    }

    return new Intl.NumberFormat('ru-RU').format(price)
}

function clampQuantity(value: number, max: number) {
    if (!Number.isFinite(value)) {
        return 1
    }

    return Math.min(Math.max(Math.trunc(value), 1), max)
}

function resetModalState() {
    currentImageIndex.value = 0
    quantity.value = 1
}

function goToImage(index: number) {
    if (!hasImages.value) {
        return
    }

    currentImageIndex.value = index
}

function nextImage() {
    if (!hasMultipleImages.value) {
        return
    }

    currentImageIndex.value = (currentImageIndex.value + 1) % totalImages.value
}

function prevImage() {
    if (!hasMultipleImages.value) {
        return
    }

    currentImageIndex.value = (currentImageIndex.value - 1 + totalImages.value) % totalImages.value
}

function increment() {
    quantity.value = clampQuantity(quantity.value + 1, maxQuantity.value)
}

function decrement() {
    quantity.value = clampQuantity(quantity.value - 1, maxQuantity.value)
}

function normalizeQuantity() {
    quantity.value = clampQuantity(quantity.value, maxQuantity.value)
}

function handleAddToCart() {
    if (!props.product || typeof props.product.price !== 'number') {
        return
    }

    normalizeQuantity()

    const cartProduct: CartProduct = {
        id: props.product.id,
        name: props.product.name,
        price: props.product.price,
        images: resolvedImages.value
            .filter((image): image is ProductImage & { url: string } => typeof image.url === 'string')
            .map((image) => ({ url: image.url })),
    }

    addToCart(cartProduct, quantity.value)
}
</script>

<template>
    <Modal v-model="isOpen">
        <div v-if="props.product" class="product-modal">
            <div class="product-head">
                <div class="product-head__content">
                    <p class="product-head__eyebrow">Карточка товара</p>
                    <h2 class="product-title">{{ props.product.name }}</h2>
                </div>
            </div>

            <div class="product-body">
                <section class="product-gallery" aria-label="Галерея изображений товара">
                    <div class="product-gallery__frame">
                        <img v-if="currentImageUrl" :src="currentImageUrl" :alt="props.product.name"
                            class="product-gallery__image" />
                        <div v-else class="product-gallery__empty">
                            Изображение отсутствует
                        </div>

                        <div v-if="hasMultipleImages" class="product-gallery__controls">
                            <button type="button" class="product-gallery__arrow" aria-label="Предыдущее изображение"
                                @click="prevImage">
                                &lt;
                            </button>
                            <span class="product-gallery__counter">
                                {{ currentImageIndex + 1 }} / {{ totalImages }}
                            </span>
                            <button type="button" class="product-gallery__arrow" aria-label="Следующее изображение"
                                @click="nextImage">
                                &gt;
                            </button>
                        </div>
                    </div>

                    <div v-if="hasMultipleImages" class="product-gallery__thumbs">
                        <button v-for="(image, index) in resolvedImages" :key="image.id ?? `${image.url}-${index}`"
                            type="button" class="product-gallery__thumb"
                            :class="{ 'product-gallery__thumb--active': index === currentImageIndex }"
                            :aria-label="`Показать изображение ${index + 1}`" @click="goToImage(index)">
                            <img v-if="image.url"
                                :src="image.url.startsWith('http') ? image.url : `${API_BASE_URL}${image.url}`"
                                :alt="`${props.product.name} ${index + 1}`" class="product-gallery__thumb-image" />
                            <span v-else class="product-gallery__thumb-dot" />
                        </button>
                    </div>
                </section>

                <section class="product-info">
                    <div class="product-status">
                        <span class="product-status__label">Наличие</span>
                        <span class="product-stock" :class="availability.className">
                            {{ availability.label }}
                        </span>
                    </div>

                    <p v-if="props.product.description" class="product-description">
                        {{ props.product.description }}
                    </p>

                    <div v-if="productMetaItems.length > 0" class="product-meta">
                        <div v-for="item in productMetaItems" :key="item.label" class="product-meta__row">
                            <span class="product-meta__label">{{ item.label }}</span>
                            <span class="product-meta__value">
                                <span v-if="item.tone === 'color' && item.colorCode" class="product-meta__color"
                                    :style="{ backgroundColor: item.colorCode }" aria-hidden="true" />
                                {{ item.value }}
                                <span v-if="item.tone === 'color' && item.colorCode" class="product-meta__code">
                                    {{ item.colorCode }}
                                </span>
                            </span>
                        </div>
                    </div>

                    <div v-if="attributeItems.length > 0" class="product-attributes">
                        <h3 class="product-section-title">Характеристики</h3>
                        <div class="product-attributes__list">
                            <div v-for="attribute in attributeItems" :key="`${attribute.name}-${attribute.value}`"
                                class="product-attributes__row">
                                <span class="product-attributes__name">{{ attribute.name }}</span>
                                <span class="product-attributes__value">{{ attribute.value }}</span>
                            </div>
                        </div>
                    </div>
                </section>
            </div>

            <div class="product-footer">
                <div class="product-footer__price-block">
                    <span class="product-footer__price-label">Цена</span>
                    <div class="product-price">
                        <template v-if="typeof props.product.price === 'number'">{{ formattedPrice }} ₽</template>
                        <template v-else>{{ formattedPrice }}</template>
                    </div>
                </div>

                <div class="product-actions">
                    <div class="product-quantity">
                        <button type="button" class="qty-btn" :disabled="quantity <= 1" @click="decrement">-</button>
                        <input v-model.number="quantity" type="number" min="1" :max="maxQuantity" class="qty-input"
                            @blur="normalizeQuantity" />
                        <button type="button" class="qty-btn" :disabled="quantity >= maxQuantity" @click="increment">
                            +
                        </button>
                    </div>

                    <button type="button" class="product-cart-button" @click="handleAddToCart">
                        {{ buttonText }}
                    </button>
                </div>
            </div>
        </div>

        <div v-else class="loading">
            Загрузка...
        </div>
    </Modal>
</template>

<style scoped>
.product-modal {
    display: flex;
    flex-direction: column;
    gap: 24px;
    color: #1e1e1e;
}

.product-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    padding-right: 32px;
}

.product-head__content {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.product-head__eyebrow {
    margin: 0;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
}

.product-title {
    margin: 0;
    font-size: 30px;
    line-height: 1.15;
    font-weight: 700;
    color: #1e1e1e;
}

.product-tag {
    padding: 6px 10px;
    border: 1px solid #e5e7eb;
    border-radius: 999px;
    background: #f9fafb;
    font-size: 12px;
    font-weight: 500;
    color: #374151;
}

.product-body {
    display: grid;
    grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
    gap: 24px;
}

.product-gallery {
    display: flex;
    flex-direction: column;
    gap: 14px;
}

.product-gallery__frame {
    position: relative;
    min-height: 360px;
    padding: 18px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background: #f9fafb;
}

.product-gallery__image {
    width: 100%;
    height: 100%;
    min-height: 320px;
    max-height: 420px;
    object-fit: contain;
    display: block;
}

.product-gallery__empty {
    min-height: 320px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px dashed #d1d5db;
    border-radius: 10px;
    color: #6b7280;
    font-size: 14px;
    background: #ffffff;
}

.product-gallery__controls {
    position: absolute;
    left: 18px;
    right: 18px;
    bottom: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.product-gallery__arrow {
    width: 40px;
    height: 40px;
    border: 1px solid rgba(255, 255, 255, 0.75);
    border-radius: 999px;
    background: rgba(30, 30, 30, 0.8);
    color: #ffffff;
    cursor: pointer;
    font-size: 18px;
    line-height: 1;
    transition: transform 0.2s ease, background-color 0.2s ease;
}

.product-gallery__arrow:hover {
    background: #1e1e1e;
}

.product-gallery__arrow:active {
    transform: scale(0.98);
}

.product-gallery__counter {
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.92);
    color: #1e1e1e;
    font-size: 13px;
    font-weight: 600;
}

.product-gallery__thumbs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(64px, 1fr));
    gap: 10px;
}

.product-gallery__thumb {
    min-height: 64px;
    padding: 6px;
    border: 1px solid #d1d5db;
    border-radius: 10px;
    background: #ffffff;
    cursor: pointer;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

.product-gallery__thumb:hover {
    border-color: #9ca3af;
}

.product-gallery__thumb--active {
    border-color: #1e1e1e;
    box-shadow: 0 0 0 1px #1e1e1e inset;
}

.product-gallery__thumb:active {
    transform: scale(0.98);
}

.product-gallery__thumb-image {
    width: 100%;
    height: 100%;
    min-height: 50px;
    object-fit: contain;
    display: block;
}

.product-gallery__thumb-dot {
    width: 10px;
    height: 10px;
    margin: 0 auto;
    display: block;
    border-radius: 999px;
    background: #9ca3af;
}

.product-info {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.product-status {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.product-status__label {
    font-size: 13px;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.product-stock {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
}

.product-stock--available {
    background: #ecfdf5;
    color: #166534;
}

.product-stock--unavailable {
    background: #fef2f2;
    color: #b91c1c;
}

.product-stock--order {
    background: #f3f4f6;
    color: #374151;
}

.product-description {
    margin: 0;
    color: #374151;
    line-height: 1.7;
    font-size: 15px;
}

.product-meta {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background: #ffffff;
}

.product-meta__row {
    display: grid;
    grid-template-columns: minmax(110px, 140px) minmax(0, 1fr);
    gap: 12px;
}

.product-meta__label {
    color: #6b7280;
    font-size: 14px;
}

.product-meta__value {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    color: #1e1e1e;
    font-size: 14px;
    font-weight: 500;
}

.product-meta__color {
    width: 14px;
    height: 14px;
    border: 1px solid rgba(17, 24, 39, 0.14);
    border-radius: 999px;
    flex-shrink: 0;
}

.product-meta__code {
    color: #6b7280;
    font-size: 12px;
    font-weight: 500;
}

.product-attributes {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.product-section-title {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #1e1e1e;
}

.product-attributes__list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background: #f9fafb;
}

.product-attributes__row {
    display: grid;
    grid-template-columns: minmax(120px, 160px) minmax(0, 1fr);
    gap: 12px;
}

.product-attributes__name {
    color: #6b7280;
    font-size: 14px;
}

.product-attributes__value {
    color: #1e1e1e;
    font-size: 14px;
    font-weight: 500;
}

.product-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 18px 20px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background: #f9fafb;
}

.product-footer__price-block {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.product-footer__price-label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 500;
}

.product-price {
    font-size: 30px;
    line-height: 1;
    font-weight: 700;
    color: #1e1e1e;
}

.product-actions {
    display: flex;
    align-items: center;
    gap: 24px;
}

.product-quantity {
    --qty-height: 44px;

    display: inline-flex;
    align-items: stretch;
    height: var(--qty-height);
    border: 1px solid #1e1e1e;
    border-radius: 10px;
    overflow: hidden;
    background: #ffffff;
}

.qty-btn {
    width: 44px;
    height: 100%;
    padding: 0;
    border: none;
    box-sizing: border-box;
    background: #1e1e1e;
    cursor: pointer;
    font-size: 18px;
    line-height: 1;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease, transform 0.2s ease;
}

.qty-btn:hover:not(:disabled) {
    background: rgb(60, 60, 60);
}

.qty-btn:disabled {
    background: #9ca3af;
    cursor: not-allowed;
}

.qty-input {
    width: 50px;
    height: 100%;
    padding: 0;
    border: none;
    border-left: 1px solid #1e1e1e;
    border-right: 1px solid #1e1e1e;
    box-sizing: border-box;
    text-align: center;
    font-size: 15px;
    font-weight: 600;
    color: #1e1e1e;
    background: transparent;
}

.qty-input:focus {
    outline: none;
}

.qty-input::-webkit-outer-spin-button,
.qty-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.qty-input[type='number'] {
    -moz-appearance: textfield;
    appearance: textfield;
}

.product-cart-button {
    min-width: 220px;
    padding: 14px 20px;
    border: 1px solid #1e1e1e;
    border-radius: 10px;
    background: #1e1e1e;
    color: #ffffff;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    transition: background-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
}

.product-cart-button:hover {
    background: #111827;
}

.product-cart-button:active {
    transform: scale(0.96);
}

.loading {
    text-align: center;
    padding: 40px;
    color: #6b7280;
}

@media (max-width: 900px) {
    .product-head {
        padding-right: 0;
        flex-direction: column;
    }

    .product-body {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 640px) {
    .product-title {
        font-size: 24px;
    }

    .product-gallery__frame {
        min-height: 280px;
        padding: 14px;
    }

    .product-gallery__image,
    .product-gallery__empty {
        min-height: 240px;
    }

    .product-meta__row,
    .product-attributes__row {
        grid-template-columns: 1fr;
        gap: 4px;
    }

    .product-footer {
        flex-direction: column;
        align-items: stretch;
    }

    .product-actions {
        width: 100%;
        flex-direction: column;
        align-items: stretch;
        gap: 16px;
    }

    .product-quantity {
        width: 100%;
    }

    .qty-btn {
        flex: 1;
    }

    .qty-input {
        width: auto;
        flex: 1;
    }

    .product-cart-button {
        width: 100%;
        min-width: 0;
    }

    .product-price {
        font-size: 26px;
    }
}
</style>
