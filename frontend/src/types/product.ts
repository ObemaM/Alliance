export interface ProductRelation {
  id: number
  name: string
}

export interface ProductColor extends ProductRelation {
  code: string | null
}

export interface ProductImage {
  id: number
  product_id: number
  url: string | null
}

export interface ProductAttributeDefinition {
  id: number
  name: string
}

export interface ProductAttribute {
  product_id: number
  attribute_id: number
  value_text: string | null
  attribute: ProductAttributeDefinition | null
}

export interface Product {
  id: number
  name: string
  description: string | null
  category_id: number | null
  pack_quantity: number | null
  quantity: number | null
  price: number | null
  weight: string | null
  color_id: number | null
  material_id: number | null
  country_id: number | null
  purpose: string | null
  created_at: string | null
  updated_at: string | null
  category: ProductRelation | null
  color: ProductColor | null
  material: ProductRelation | null
  country: ProductRelation | null
  product_attributes: ProductAttribute[]
  images: ProductImage[]
}
