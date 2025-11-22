# 🚀 PUSH RÁPIDO A GITHUB

## ⚡ OPCIÓN 1: GitHub Desktop (30 segundos)

1. Abre **GitHub Desktop**
2. Menu: `File → Add Local Repository`
3. Selecciona: `C:\Users\alber\OneDrive\Documentos\memoria_claude\metodo`
4. Click: **"Push origin"** (botón azul)
5. ¡Listo! ✅

---

## 🔧 OPCIÓN 2: Terminal (2 minutos)

Abre PowerShell o CMD y ejecuta:

```powershell
# Ir al directorio del proyecto
cd "C:\Users\alber\OneDrive\Documentos\memoria_claude\metodo"

# Push a GitHub
git push -u origin main
```

**Te pedirá credenciales:**
- Usuario: `albertomartinezdelacasa`
- Contraseña: Tu contraseña de GitHub

---

## 🔑 SI FALLA LA CONTRASEÑA

GitHub ya no acepta contraseñas simples. Necesitas un **Personal Access Token**:

1. Ve a: https://github.com/settings/tokens
2. Click: **"Generate new token (classic)"**
3. Dale un nombre: "Metodo Comedia Deploy"
4. Selecciona: **repo** (marca la casilla)
5. Click: **"Generate token"**
6. **COPIA EL TOKEN** (solo lo verás una vez)

Luego, cuando hagas `git push`, usa:
- Usuario: `albertomartinezdelacasa`
- Contraseña: **PEGA EL TOKEN AQUÍ** (en lugar de tu contraseña)

---

## ✅ VERIFICAR QUE FUNCIONÓ

Después del push, ve a:
```
https://github.com/albertomartinezdelacasa/metodo
```

Deberías ver todos los archivos del proyecto.

---

## 🎯 SIGUIENTE PASO: RENDER.COM

Una vez el push esté completo, continúa con el deploy en Render:

1. Ve a: https://render.com
2. Sign up with GitHub
3. New → Web Service
4. Conecta el repo "metodo"
5. Configura variables de entorno
6. Deploy!

**Guía completa:** Lee `DEPLOYMENT_GUIDE.md`

---

**¿Problema con el push?**
- Verifica que estés logueado con la cuenta correcta
- Usa GitHub Desktop si tienes problemas con la terminal
- Genera un Personal Access Token si falla la contraseña
