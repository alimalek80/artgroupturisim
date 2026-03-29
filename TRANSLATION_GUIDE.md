# How to Translate Content in Django Admin

## Overview
Your Art Tourism website now supports **3 languages**:
- 🇬🇧 **English** (default)
- 🇹🇷 **Turkish**
- 🇷🇺 **Russian**

## Adding/Editing Tours with Translations

When you add or edit a tour in the Django admin, you'll see **language tabs** at the top of translatable fields.

### Step-by-Step Guide:

#### 1. Access the Django Admin
```
http://localhost:8000/admin/
```

#### 2. Go to Tours → Add Tour (or edit existing)

#### 3. You'll See Language Tabs
For each translatable field, you'll see tabs like this:
```
[English] [Türkçe] [Русский]
```

#### 4. Fill in Content for Each Language

**Example for Tour Title:**
- Click **[English]** tab → Enter: "Bosphorus Sunset Cruise"
- Click **[Türkçe]** tab → Enter: "Boğaz Gün Batımı Turu"
- Click **[Русский]** tab → Enter: "Круиз На Закате По Босфору"

**Example for Description:**
- **[English]**: "Enjoy a magical sunset cruise along the Bosphorus..."
- **[Türkçe]**: "Boğaz'da büyülü bir gün batımı turunda deneyim yaşayın..."
- **[Русский]**: "Насладитесь волшебным круизом на закате вдоль Босфора..."

### Translatable Fields

The following fields support multi-language input:

**Tour Fields:**
- ✅ Title
- ✅ Subtitle
- ✅ Short Description
- ✅ Description
- ✅ Duration Text
- ✅ Pickup Information
- ✅ Itinerary Description
- ✅ Meta Description (SEO)

**Related Models:**
- ✅ **Included Items** → item text
- ✅ **Excluded Items** → item text
- ✅ **Tour Notes** → content
- ✅ **Items to Bring** → item text
- ✅ **Itinerary Items** → title, description, location
- ✅ **Pickup Locations** → name, address, instructions
- ✅ **Cancellation Policy Rules** → description

**Categories & Options:**
- ✅ **Tour Categories** → name, description
- ✅ **Languages** → name
- ✅ **Accessibility Options** → name, description

## Important Notes

### English is Required ⚠️
- **English** content is **required** for all translatable fields
- Turkish and Russian translations are **optional**
- If a translation is missing, the English version will be displayed as fallback

### Inline Forms (Within Tour Admin)
When adding items like "Included Items" or "Itinerary Items" via inline forms:
1. You'll see language tabs for each translatable field
2. Fill in at least the English version
3. Add Turkish/Russian as needed

### Auto-Slug Generation
- The `slug` field is automatically generated from the **English title**
- You can customize it if needed

## How Translations Display on the Website

### URL Structure:
- **English**: `https://yoursite.com/tours/bosphorus-sunset-cruise/`
- **Turkish**: `https://yoursite.com/tr/tours/bosphorus-sunset-cruise/`
- **Russian**: `https://yoursite.com/ru/tours/bosphorus-sunset-cruise/`

### Language Detection:
1. Users select language from navbar dropdown (🇬🇧 English / 🇹🇷 Türkçe / 🇷🇺 Русский)
2. Website displays tour content in selected language
3. Fallback to English if translation missing

## Example Workflow

### Adding a New "Cappadocia Hot Air Balloon Tour"

1. **Go to**: Admin → Tours → Add Tour
2. **Basic Info Tab** (English):
   - Title: "Cappadocia Hot Air Balloon Ride"
   - Subtitle: "Soar Above Fairy Chimneys at Sunrise"
   - Short Description: "Experience the magic of Cappadocia from above..."

3. **Switch to Türkçe Tab**:
   - Title: "Kapadokya Sıcak Hava Balonu Turu"
   - Subtitle: "Gün Doğumunda Peri Bacalarının Üzerinde Uçun"
   - Short Description: "Kapadokya'nın büyüsünü yukarıdan deneyimleyin..."

4. **Switch to Русский Tab**:
   - Title: "Полет На Воздушном Шаре В Каппадокии"
   - Subtitle: "Парите Над Сказочными Дымоходами На Рассвете"
   - Short Description: "Испытайте волшебство Каппадокии сверху..."

5. **Fill in Non-Translatable Fields** (same for all languages):
   - Duration: 2 hours
   - Difficulty: Easy
   - Max Participants: 20
   - Price: (handled in bookings app)

6. **Add Inline Items**:
   - **Included Items**:
     - [English]: "Hotel pickup & drop-off"
     - [Türkçe]: "Otel alış ve bırakma"
     - [Русский]: "Трансфер из отеля и обратно"

7. **Click Save**

## Tips & Best Practices

### ✅ DO:
- Always fill in English content first
- Use natural, culturally appropriate translations
- Keep formatting consistent across languages
- Preview the website in each language before publishing

### ❌ DON'T:
- Don't use online translators blindly (review for accuracy)
- Don't mix languages within the same field
- Don't leave English fields empty

## Checking Your Work

1. **Save your tour**
2. **Open website** in new tab
3. **Change language** using navbar dropdown
4. **Navigate to your tour** and verify translations display correctly

## Troubleshooting

**Problem**: "I don't see language tabs"
- **Solution**: Make sure `modeltranslation` is in INSTALLED_APPS and migrations are applied

**Problem**: "Only seeing English content on website"
- **Solution**: Check that you saved content in the correct language tab in admin

**Problem**: "Translation tabs not showing for a field"
- **Solution**: That field might not be registered as translatable (check `tours/translation.py`)

## Need Help?

### Check These Files:
- `/tours/translation.py` → Which fields are translatable
- `/tours/admin.py` → Admin interface configuration
- `/artturisim/settings.py` → Language settings (LANGUAGES, MODELTRANSLATION_*)

### Management Commands:
```bash
# Update translation fields from existing data
python manage.py update_translation_fields

# Compile translation messages (for UI text)
python manage.py compilemessages --locale=tr --locale=ru
```

---

**Happy Translating! 🌍**
