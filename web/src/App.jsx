import { useEffect, useState } from "react";
import { supabase } from "./supabaseClient";
import { initChatwoot } from "./chatwoot";

const TABLE_NAME = "profiles";

export default function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [profileName, setProfileName] = useState("");

  useEffect(() => {
    initChatwoot();

    supabase.auth.getSession().then(({ data }) => {
      setSession(data.session ?? null);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, nextSession) => {
      setSession(nextSession);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signIn = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setStatus("");

    const { error: signInError } = await supabase.auth.signInWithOtp({ email });
    setLoading(false);

    if (signInError) {
      setError(signInError.message);
      return;
    }

    setStatus("Te enviamos un magic link a tu correo.");
    setEmail("");
  };

  const signOut = async () => {
    setLoading(true);
    const { error: signOutError } = await supabase.auth.signOut();
    setLoading(false);
    if (signOutError) setError(signOutError.message);
  };

  const saveProfile = async (e) => {
    e.preventDefault();
    if (!session?.user?.id) return;
    setLoading(true);
    setError("");
    setStatus("");

    const payload = {
      id: session.user.id,
      email: session.user.email,
      full_name: profileName,
      updated_at: new Date().toISOString(),
    };

    const { error: upsertError } = await supabase
      .from(TABLE_NAME)
      .upsert(payload, { onConflict: "id" });

    setLoading(false);
    if (upsertError) {
      setError(upsertError.message);
      return;
    }
    setStatus("Perfil guardado en Supabase.");
  };

  return (
    <main className="container">
      <h1>FREELANCE • React + Supabase + Chatwoot</h1>

      {!session ? (
        <form className="card" onSubmit={signIn}>
          <h2>Iniciar sesión</h2>
          <p>Login con magic link (Supabase Auth).</p>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="tu@email.com"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? "Enviando..." : "Enviar magic link"}
          </button>
        </form>
      ) : (
        <section className="card">
          <h2>Sesión activa</h2>
          <p>
            <strong>Usuario:</strong> {session.user.email}
          </p>
          <form onSubmit={saveProfile}>
            <input
              type="text"
              value={profileName}
              onChange={(e) => setProfileName(e.target.value)}
              placeholder="Nombre para perfil"
            />
            <button type="submit" disabled={loading}>
              {loading ? "Guardando..." : "Guardar perfil"}
            </button>
          </form>
          <button className="secondary" onClick={signOut} disabled={loading}>
            Cerrar sesión
          </button>
        </section>
      )}

      {status ? <p className="ok">{status}</p> : null}
      {error ? <p className="error">{error}</p> : null}

      <section className="card">
        <h3>Config requerida</h3>
        <p>
          Define en <code>web/.env</code>: <code>VITE_SUPABASE_URL</code>,{" "}
          <code>VITE_SUPABASE_ANON_KEY</code>, <code>VITE_CHATWOOT_BASE_URL</code>{" "}
          y <code>VITE_CHATWOOT_WEBSITE_TOKEN</code>.
        </p>
      </section>
    </main>
  );
}
