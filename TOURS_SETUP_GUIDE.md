# Tours App - Setup and Migration Instructions

## Step 1: Create and Apply Migrations

# Make sure your virtual environment is activated
# Then run:

python manage.py makemigrations tours
python manage.py migrate

## Step 2: Create a Superuser (if you haven't already)

python manage.py createsuperuser

## Step 3: Run the Development Server

python manage.py runserver

## Step 4: Access the Admin Panel

# Visit: http://127.0.0.1:8000/admin/
# Log in with your superuser credentials

## Step 5: Add Sample Data

In the Django admin, create:
1. Tour Categories (e.g., Adventure, Cultural, Food & Wine)
2. Languages (e.g., English, Spanish, French)
3. Accessibility Options (e.g., Wheelchair accessible, Audio guide available)
4. Create your first tour with all related content

## Step 6: View Tours

# Tour List: http://127.0.0.1:8000/tours/
# Tour Detail: http://127.0.0.1:8000/tours/your-tour-slug/

---

## URL Structure

- `/tours/` - List all tours with filters and search
- `/tours/featured/` - Featured tours (can be used on homepage)
- `/tours/<slug>/` - Tour detail page

---

## Media Files Configuration

The tours app uses ImageField for tour images. Make sure your settings.py has:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

And in your main urls.py (already configured):
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Future Bookings App Integration Points

When you're ready to integrate with the bookings app:

### In tours/models.py:
- `TourAvailability` model is ready to be queried and updated by bookings app
- `Tour.max_participants`, `Tour.min_participants`, `Tour.booking_cutoff_hours` are available
- All participant and pricing data can be stored in bookings app

### In tours/views.py - TourDetailView:
- `context['participant_types']` provides structure for booking form
- `context['available_dates']` provides next 30 available dates
- Ready to pass tour data to booking form/modal

### Suggested Bookings App Integration Flow:
1. User selects tour, date, and participants on tour detail page
2. JavaScript sends data to bookings app API endpoint
3. Bookings app:
   - Validates availability via `TourAvailability.objects.filter(...)`
   - Calculates pricing (all financial logic here)
   - Creates booking record
   - Updates `TourAvailability.slots_available`
4. Returns booking confirmation

---

## Admin Panel Features

### Tour Admin:
- Fieldsets organized by purpose
- 9 inline forms for related content
- Filter by status, category, difficulty
- Search by title, description
- Auto-populate slug from title
- Rich review display
- Horizontal filter for many-to-many relationships

### Quick Content Entry:
Use inlines to add everything from one page:
- Images
- Itinerary steps
- Included/excluded items
- Notes
- Items to bring
- Pickup locations
- Available dates
- Cancellation rules

---

## Tailwind CSS Considerations

The templates use Tailwind utility classes. Make sure your Tailwind build includes:
- Responsive breakpoints (md:, lg:)
- Custom colors (orange-500, slate-900, etc.)
- Rounded utilities (rounded-2xl, rounded-3xl)
- Shadow utilities (shadow-lg, shadow-xl)

Run your Tailwind build process:
```bash
# If you have build scripts already
npm run build:css
# or
./build-tailwind-dev.sh
```

---

## Model Relationships Overview

```
Tour (Main Model)
├── Many-to-Many: TourCategory
├── Many-to-Many: Language
├── Many-to-Many: AccessibilityOption
├── One-to-Many: TourImage
├── One-to-Many: IncludedItem
├── One-to-Many: ExcludedItem
├── One-to-Many: TourNote
├── One-to-Many: ItemToBring
├── One-to-Many: ItineraryItem
├── One-to-Many: TourAvailability
├── One-to-Many: CancellationPolicyRule
└── One-to-Many: PickupLocation
```

---

## Best Practices Implemented

✅ Use of `get_absolute_url()` for Tour model
✅ Proper `related_name` on all ForeignKey relationships
✅ `verbose_name` and `verbose_name_plural` for better admin UI
✅ Custom `__str__` methods for all models
✅ Ordering in Meta classes
✅ Database indexes on frequently queried fields
✅ Slug auto-generation
✅ Query optimization with prefetch_related
✅ Proper separation of concerns (no business logic in models)
✅ Comments indicating future integration points

---

## Extending the Tour App

### Add Search by Location:
Add `location` field to Tour model, then filter by it in TourListView

### Add Tour Reviews:
Create a separate `TourReview` model that updates `Tour.review_count` and `Tour.rating_average`

### Add Wishlist/Favorites:
Create `TourFavorite` model with ForeignKey to Tour and User

### Add Tour Dates as Calendar:
Integrate a date picker library and fetch available dates via AJAX

### Add Share Functionality:
Add social sharing buttons on tour detail page

### Add Tour Comparison:
Allow users to compare multiple tours side-by-side
