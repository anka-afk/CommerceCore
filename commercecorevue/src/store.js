// store.js
import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state() {
    return {
      cartItems: [],
    };
  },
  mutations: {
    setCartItems(state, items) {
      state.cartItems = items;
    },
    addToCart(state, item) {
      const existingItem = state.cartItems.find(
        (i) => i.product.product_id === item.product.product_id
      );
      if (existingItem) {
        existingItem.quantity += item.quantity;
      } else {
        state.cartItems.push(item);
      }
    },
    removeFromCart(state, productId) {
      state.cartItems = state.cartItems.filter(
        (item) => item.product.product_id !== productId
      );
    },
    clearCart(state) {
      state.cartItems = [];
    },
  },
  actions: {
    async fetchCartItems({ commit }) {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/cart/");
        commit("setCartItems", response.data.items);
      } catch (error) {
        console.error("Failed to fetch cart items:", error);
      }
    },
    async addItemToCart({ commit }, item) {
      try {
        await axios.post("http://127.0.0.1:8000/api/cart/update_quantity/", {
          product_id: item.product.product_id,
          quantity: item.quantity,
        });
        commit("addToCart", item);
      } catch (error) {
        console.error("Failed to add item to cart:", error);
      }
    },
    async removeItemFromCart({ commit }, productId) {
      try {
        await axios.post("http://127.0.0.1:8000/api/cart/remove_item/", {
          product_id: productId,
        });
        commit("removeFromCart", productId);
      } catch (error) {
        console.error("Failed to remove item from cart:", error);
      }
    },
    clearCartItems({ commit }) {
      commit("clearCart");
    },
  },
  getters: {
    cartItems: (state) => state.cartItems,
    totalAmount: (state) =>
      state.cartItems.reduce(
        (total, item) => total + item.product.price * item.quantity,
        0
      ),
    getOrderById: (state) => (id) => {
      return state.orders.find((order) => order.number === id);
    },
  },
});
