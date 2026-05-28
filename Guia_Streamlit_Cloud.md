# Guía: Publicar tu app en Streamlit Cloud
## De cero a link compartible en ~15 minutos

---

## LO QUE VAS A LOGRAR

Al final tendrás un link como:
```
https://tuusuario.streamlit.app
```
Cualquier persona lo abre desde su navegador — sin instalar nada.

---

## PASO 1 — Crear cuenta en GitHub (3 min)

1. Ve a **https://github.com**
2. Clic en **"Sign up"** (arriba a la derecha)
3. Ingresa:
   - Tu correo electrónico
   - Una contraseña
   - Un nombre de usuario (ej: `juan-calidad`, `empresa-spc`)
4. Verifica tu correo (te llega un código de 6 dígitos)
5. En las preguntas de configuración, selecciona **"Free"** (gratuito)

---

## PASO 2 — Crear un repositorio (2 min)

Un repositorio es la carpeta donde vive tu app en GitHub.

1. Una vez dentro de GitHub, clic en el botón verde **"New"** (o ve a https://github.com/new)
2. Completa:
   - **Repository name:** `control-estadistico-proceso` (sin espacios, usa guiones)
   - **Description:** `App de Control Estadístico de Proceso` (opcional)
   - **Visibility:** ✅ **Public** (necesario para el plan gratuito de Streamlit)
3. ✅ Marca **"Add a README file"**
4. Clic en **"Create repository"** (botón verde abajo)

---

## PASO 3 — Subir el archivo de la app (3 min)

1. Dentro de tu repositorio recién creado, clic en **"Add file"** → **"Upload files"**
2. Arrastra o selecciona el archivo **`App2.py`**
3. Abajo, en "Commit changes", escribe:
   - `Subir app de control estadístico`
4. Clic en **"Commit changes"** (botón verde)

---

## PASO 4 — Crear el archivo de dependencias (2 min)

Streamlit necesita saber qué librerías instalar.

1. En tu repositorio, clic en **"Add file"** → **"Create new file"**
2. En el nombre del archivo escribe exactamente: `requirements.txt`
3. En el contenido pega esto:

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
scipy>=1.11.0
```

4. Clic en **"Commit new file"** (botón verde abajo)

Tu repositorio ahora debe tener estos 3 archivos:
```
📁 control-estadistico-proceso/
   ├── README.md
   ├── App2.py
   └── requirements.txt
```

---

## PASO 5 — Crear cuenta en Streamlit Cloud (2 min)

1. Ve a **https://share.streamlit.io**
2. Clic en **"Sign up"**
3. Selecciona **"Continue with GitHub"** (importante: usa la misma cuenta que creaste)
4. Autoriza el acceso cuando te lo pida

---

## PASO 6 — Desplegar la app (3 min)

1. Una vez dentro de Streamlit Cloud, clic en **"New app"**
2. Completa el formulario:
   - **Repository:** selecciona `tuusuario/control-estadistico-proceso`
   - **Branch:** `main`
   - **Main file path:** `App2.py`
3. Clic en **"Deploy!"** (botón azul)
4. Espera 2-4 minutos mientras instala las dependencias (verás logs en pantalla)
5. Cuando aparezca tu app funcionando, ¡listo!

---

## TU LINK PARA COMPARTIR

Al terminar tendrás un link como:
```
https://tuusuario-control-estadistico-proceso-app2-xxxxx.streamlit.app
```

Puedes personalizarlo desde **Settings → General → Custom subdomain** en Streamlit Cloud.

---

## CÓMO ACTUALIZAR LA APP EN EL FUTURO

Cuando quieras subir una versión nueva de `App2.py`:
1. Ve a tu repositorio en GitHub
2. Clic sobre `App2.py` → clic en el ícono del lápiz ✏️ (o sube el archivo nuevo)
3. Streamlit Cloud detecta el cambio y se actualiza automáticamente en ~1 minuto

---

## RESUMEN RÁPIDO

| Paso | Acción | Tiempo |
|------|--------|--------|
| 1 | Crear cuenta GitHub en github.com | 3 min |
| 2 | Crear repositorio público | 2 min |
| 3 | Subir App2.py | 3 min |
| 4 | Crear requirements.txt | 2 min |
| 5 | Crear cuenta Streamlit Cloud | 2 min |
| 6 | Hacer Deploy | 3 min |
| **Total** | | **~15 min** |

---

## LINKS IMPORTANTES

- Crear cuenta GitHub: https://github.com
- Streamlit Cloud: https://share.streamlit.io
- Plan gratuito incluye: apps públicas ilimitadas, 1 app privada

---

*Una vez publicada, cualquier persona con el link puede acceder desde PC, celular o tablet sin instalar nada.*
