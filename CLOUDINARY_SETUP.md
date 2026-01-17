# 🖼️ Configuration Cloudinary pour Railway

## Problème
Les images des produits disparaissent à chaque déploiement sur Railway car le système de fichiers est **éphémère** (temporaire).

## Solution
Utiliser **Cloudinary** - un service gratuit de stockage cloud pour les images.

---

## 📋 Étapes de Configuration

### 1. Créer un compte Cloudinary (GRATUIT)

1. Allez sur https://cloudinary.com/users/register_free
2. Créez un compte gratuit avec votre email
3. Vérifiez votre email et connectez-vous

### 2. Obtenir vos identifiants Cloudinary

1. Une fois connecté, vous serez sur le **Dashboard**
2. Notez ces 3 informations importantes :
   - **Cloud Name** (ex: `dxyz123abc`)
   - **API Key** (ex: `123456789012345`)
   - **API Secret** (ex: `abcdefghijklmnopqrstuvwxyz123`)

3. Vous verrez aussi une URL complète comme :
   ```
   cloudinary://123456789012345:abcdefghijklmnopqrstuvwxyz123@dxyz123abc
   ```

### 3. Configurer les variables d'environnement sur Railway

1. Allez sur https://railway.app et ouvrez votre projet
2. Cliquez sur votre service Django
3. Allez dans l'onglet **Variables**
4. Ajoutez cette variable (utilisez votre propre URL Cloudinary) :

   ```
   CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
   ```
   
   Par exemple :
   ```
   CLOUDINARY_URL=cloudinary://123456789012345:abcdefghijklmnopqrstuvwxyz123@dxyz123abc
   ```

5. Cliquez sur **Add** puis **Deploy**

### 4. Vérifier que ça fonctionne

Après le redéploiement :

1. Regardez les logs Railway - vous devriez voir :
   ```
   ✅ Cloudinary storage activated for media files
   ```

2. Ajoutez une image de produit dans l'admin Django
3. L'URL de l'image sera maintenant sur Cloudinary (ex: `https://res.cloudinary.com/...`)
4. Redéployez votre application - l'image sera toujours là ! ✅

---

## 🎁 Avantages

- ✅ **Images persistantes** - ne disparaissent plus
- ✅ **Gratuit** - 10 GB de stockage, 25k transformations/mois
- ✅ **CDN rapide** - vos images se chargent rapidement partout dans le monde
- ✅ **Optimisation automatique** - Cloudinary optimise vos images
- ✅ **Transformations** - redimensionnement, recadrage, etc.

---

## 📌 Notes Importantes

### Plan gratuit Cloudinary :
- 25 crédits/mois
- 10 GB de stockage
- 25k transformations/mois
- Largement suffisant pour un site de pépinière !

### Si vous dépassez les limites :
Le plan payant commence à 89$/an mais pour un petit site, le plan gratuit suffit.

---

## 🔧 Dépannage

### Les images ne s'affichent pas après la configuration ?

1. **Vérifiez les logs Railway** :
   - Cherchez le message "✅ Cloudinary storage activated"
   - Si vous voyez "⚠️ WARNING: Using ephemeral file storage", la variable CLOUDINARY_URL n'est pas configurée

2. **Vérifiez la variable d'environnement** :
   - Format correct : `cloudinary://API_KEY:API_SECRET@CLOUD_NAME`
   - Pas d'espaces avant ou après
   - Tous les caractères spéciaux sont inclus

3. **Redéployez** après avoir ajouté la variable

### Comment migrer les images existantes ?

Les images ajoutées avant Cloudinary sont sur le système éphémère et seront perdues.
Après avoir configuré Cloudinary :

1. Téléchargez les images localement (si vous les avez)
2. Re-téléchargez-les via l'interface admin Django
3. Elles seront maintenant sur Cloudinary et persistantes

---

## 📞 Support

- Documentation Cloudinary Django : https://cloudinary.com/documentation/django_integration
- Support Cloudinary : https://support.cloudinary.com/

---

**Une fois configuré, vous n'aurez plus jamais à re-charger vos images après un déploiement ! 🎉**
