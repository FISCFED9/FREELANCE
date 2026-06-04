# FREELANCE

Sistema de agentes + base web con **React + Supabase + Chatwoot**.

## Web app (`web/`)

Incluye:
- Auth con magic link (Supabase)
- Guardado de perfil en tabla `profiles`
- Widget de Chatwoot embebido
- Lista para desplegar en Vercel

### 1) Configurar variables

1. Copia `web/.env.example` a `web/.env`
2. Completa:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - `VITE_CHATWOOT_BASE_URL`
   - `VITE_CHATWOOT_WEBSITE_TOKEN`

### 2) Crear tabla en Supabase

Ejecuta `web/supabase_schema.sql` en el SQL editor de tu proyecto Supabase.

### 3) Ejecutar local

```powershell
cd web
npm install
npm run dev
```

### 4) Deploy en Vercel

1. Importa el repo en Vercel
2. Root Directory: `web`
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Configura en Vercel las mismas variables `VITE_*`
