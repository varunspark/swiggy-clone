import { useEffect, useState } from "react";

const api = async (path, opts = {}, token) => {
  const res = await fetch(`/api${path}`, {
    ...opts,
    headers: { "Content-Type": "application/json", ...(token && { Authorization: `Token ${token}` }) },
  });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.json();
};

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [restaurants, setRestaurants] = useState([]);
  const [selected, setSelected] = useState(null);
  const [cart, setCart] = useState({});
  const [msg, setMsg] = useState("");

  useEffect(() => { api("/restaurants/").then(setRestaurants).catch((e) => setMsg(e.message)); }, []);

  const auth = async (kind, e) => {
    e.preventDefault();
    const body = JSON.stringify({ username: e.target.username.value, password: e.target.password.value });
    try {
      const data = await api(`/${kind}/`, { method: "POST", body });
      localStorage.setItem("token", data.token);
      setToken(data.token); setMsg("");
    } catch (err) { setMsg(err.message); }
  };

  const open = async (id) => { setCart({}); setSelected(await api(`/restaurants/${id}/`)); };
  const add = (item) => setCart((c) => ({ ...c, [item.id]: (c[item.id] || 0) + 1 }));
  const total = selected?.menu.reduce((s, i) => s + (cart[i.id] || 0) * i.price, 0) || 0;

  const placeOrder = async () => {
    const items = Object.entries(cart).map(([id, quantity]) => ({ menu_item: +id, quantity }));
    try {
      const o = await api("/orders/", { method: "POST", body: JSON.stringify({ restaurant: selected.id, items }) }, token);
      setMsg(`Order #${o.id} placed. Total ₹${o.total}`); setCart({});
    } catch (err) { setMsg(err.message); }
  };

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 720, margin: "0 auto", padding: 16 }}>
      <h1 style={{ color: "#fc8019" }}>Swiggy Clone</h1>
      {msg && <p role="status">{msg}</p>}
      {!token ? (
        <form onSubmit={(e) => auth("login", e)}>
          <input name="username" placeholder="Username" required />{" "}
          <input name="password" type="password" placeholder="Password" required />{" "}
          <button>Log in</button>{" "}
          <button type="button" onClick={(e) => auth("register", { preventDefault() {}, target: e.target.form })}>Register</button>
        </form>
      ) : (
        <button onClick={() => { localStorage.removeItem("token"); setToken(null); }}>Log out</button>
      )}

      {!selected ? (
        <section>
          <h2>Restaurants</h2>
          {restaurants.map((r) => (
            <div key={r.id} onClick={() => open(r.id)} style={{ border: "1px solid #ddd", padding: 12, margin: "8px 0", cursor: "pointer" }}>
              <strong>{r.name}</strong> ★ {r.rating}<br />{r.cuisine}, {r.address}
            </div>
          ))}
        </section>
      ) : (
        <section>
          <button onClick={() => setSelected(null)}>Back</button>
          <h2>{selected.name}</h2>
          {selected.menu.map((i) => (
            <div key={i.id} style={{ display: "flex", justifyContent: "space-between", padding: 6 }}>
              <span>{i.is_veg ? "🟢" : "🔴"} {i.name} ₹{i.price}</span>
              <button onClick={() => add(i)}>Add{cart[i.id] ? ` (${cart[i.id]})` : ""}</button>
            </div>
          ))}
          <p><strong>Total: ₹{total}</strong></p>
          <button disabled={!total || !token} onClick={placeOrder}>{token ? "Place order" : "Log in to order"}</button>
        </section>
      )}
    </main>
  );
}
