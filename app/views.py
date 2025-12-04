import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .parser import *
from .forms import CustomUserCreationForm, CustomSignupForm, ProfileUpdateForm, AptForm, AmountsForm, InfoForm, CoordsForm, ImagesForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods



def index(request):

    # Retrieve all Coords instances from the database
    all_coords = list(Coords.objects.values_list('long', 'lat'))

    # Retrieve all names from the Apt model
    all_names = list(Apt.objects.values_list('name', flat=True))

    # Retrieve all addresses from Apt model
    all_addresses = list(Apt.objects.values_list('address', flat=True))

    all_cities = get_cities(all_addresses)

    content = {
        'coords': json.dumps(all_coords),
        'names': json.dumps(all_names),
        'address': json.dumps(all_addresses),
        'cities': all_cities,
    }

    return render(request, 'index.html', content)


def browse_all(request):
    # Retrieve all addresses from Apt model
    all_addresses = list(Apt.objects.values_list('address', flat=True))

    # Retrieve all names from the Apt model
    all_names = list(Apt.objects.values_list('name', flat=True))
    
    # Retrieve all IDs (We need this for the links!)
    all_ids = list(Apt.objects.values_list('id', flat=True))  # <--- NEW

    # Retrieve all minimums from the Amounts model
    all_mins = list(Amounts.objects.values_list('minimum', flat=True))

    # Retrieve all maximums from the Amounts model
    all_maxs = list(Amounts.objects.values_list('maximum', flat=True))

    # Retrieve all links from the Info model
    all_links = list(Info.objects.values_list('url', flat=True))

    # Retrieve all images from the Image model
    all_imgs = list(Images.objects.values_list('src', flat=True))

    # Retrive all phone_number from the Info model
    all_number = list(Info.objects.values_list('phone_number', flat=True))

    content = {
        'names': json.dumps(all_names),
        'addresses': json.dumps(all_addresses),
        'ids': json.dumps(all_ids),  # <--- NEW
        'mins': json.dumps(all_mins),
        'maxs': json.dumps(all_maxs),
        'links': json.dumps(all_links),
        'imgs': json.dumps(all_imgs),
        'numbers': json.dumps(all_number),
    }
    
    return render(request, 'browseall.html', content)



def search_apts(request):
    if request.method == 'POST':
        try:
            # Retrieve form data from the request.POST dictionary
            rent_min = request.POST.get('rent_min')
            rent_max = request.POST.get('rent_max')
            city = request.POST.get('city')
            zip_code = request.POST.get('zip_code')

            # Ensure that rent_min is less than rent_max and vice-versa
            if rent_min > rent_max:
                rent_min, rent_max = rent_max, rent_min

            # Get Contents of Models
            apartments = Apt.objects.all()
            amounts = Amounts.objects.all()
            contacts = Info.objects.all()
            images = Images.objects.all()

            if city:

                # Filter apartments based on the selected city
                apartments = apartments.filter(address__icontains=city)

                # Get the IDs of the filtered apartments
                apartment_ids = apartments.values_list('id', flat=True)

                # Filter amounts, contacts, and images based on the IDs of the filtered apartments
                amounts = amounts.filter(apt_id__in=apartment_ids)
                contacts = contacts.filter(apt_id__in=apartment_ids)
                images = images.filter(apt_id__in=apartment_ids)

            if zip_code:

                # Filter apartments based on the selected zip_code
                apartments = apartments.filter(address__icontains=zip_code)

                # Get the IDs of the filtered apartments
                apartment_ids = apartments.values_list('id', flat=True)

                # Filter amounts, contacts, and images based on the IDs of the filtered apartments
                amounts = amounts.filter(apt_id__in=apartment_ids)
                contacts = contacts.filter(apt_id__in=apartment_ids)
                images = images.filter(apt_id__in=apartment_ids)

            if rent_min:

                # Filter apartments based on the entered rent_min
                amounts = amounts.filter(minimum__gte=int(rent_min))

                # Get the Apt_ids of the filtered apartments
                amt_ids = amounts.values_list('apt_id', flat=True)

                # Filter Apartments, contacts, and images based on the IDs of the filtered amounts
                apartments = apartments.filter(id__in=amt_ids)
                contacts = contacts.filter(apt_id__in=amt_ids)
                images = images.filter(apt_id__in=amt_ids)

            if rent_max:

                # Filter apartments based on the entered rent_max
                amounts = amounts.filter(minimum__lte=int(rent_max))

                # Get the Apt_ids of the filtered apartments
                amt_ids = amounts.values_list('apt_id', flat=True)

                # Filter Apartments, contacts, and images based on the IDs of the filtered amounts
                apartments = apartments.filter(id__in=amt_ids)
                contacts = contacts.filter(apt_id__in=amt_ids)
                images = images.filter(apt_id__in=amt_ids)

            # Retrieve all addresses from Apt model
            all_addresses = list(apartments.values_list('address', flat=True))

            # Retrieve all names from the Apt model
            all_names = list(apartments.values_list('name', flat=True))

            # Retrieve all minimums from the Amounts model
            all_mins = list(amounts.values_list('minimum', flat=True))

            # Retrieve all maximums from the Amounts model
            all_maxs = list(amounts.values_list('maximum', flat=True))

            # Retrieve all links from the Info model
            all_links = list(contacts.values_list('url', flat=True))

            # Retrieve all images from the Image model
            all_imgs = list(images.values_list('src', flat=True))

            # Retrieve all phone_number from the Info model
            all_number = list(contacts.values_list('phone_number', flat=True))

            content = {
                'names': json.dumps(all_names),
                'addresses': json.dumps(all_addresses),
                'mins': json.dumps(all_mins),
                'maxs': json.dumps(all_maxs),
                'links': json.dumps(all_links),
                'imgs': json.dumps(all_imgs),
                'numbers': json.dumps(all_number),
            }
            return render(request, 'browseall.html', content)
        except ValueError as e:
            return render(request, 'browseall.html')



def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST) # <--- Changed this line
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignupForm() # <--- Changed this line
    return render(request, 'registration/signup.html', {'form': form})



def view_apt(request, id):
    # Get the specific apartment
    apt = Apt.objects.get(id=id)
    
    return render(request, 'view_apt.html', {'apt': apt})


@login_required
def profile(request):
    # Try to fetch the related UserProfile; it's optional
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'profile.html', {
        'user': request.user,
        'profile': user_profile,
    })


@login_required
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user_profile, user=request.user)

    return render(request, 'edit_profile.html', {'form': form, 'profile': user_profile})


# Property Management Views

def is_landlord_or_seller(user):
    """Check if user is a landlord or seller"""
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.user_type in ['landlord', 'seller']
    except UserProfile.DoesNotExist:
        return False


@login_required
def my_properties(request):
    """List all properties owned by the logged-in landlord/seller"""
    if not is_landlord_or_seller(request.user):
        return redirect('profile')
    
    properties = Apt.objects.filter(owner=request.user)
    return render(request, 'my_properties.html', {'properties': properties})


@login_required
def add_property(request):
    """Add a new property"""
    if not is_landlord_or_seller(request.user):
        return redirect('profile')
    
    if request.method == 'POST':
        apt_form = AptForm(request.POST)
        if apt_form.is_valid():
            apt = apt_form.save(commit=False)
            apt.owner = request.user
            apt.save()
            return redirect('edit_property', apt_id=apt.id)
    else:
        apt_form = AptForm()
    
    return render(request, 'add_property.html', {'form': apt_form})


@login_required
def edit_property(request, apt_id):
    """Edit a property and its related information"""
    apt = get_object_or_404(Apt, id=apt_id)
    
    # Check if user owns this property
    if apt.owner != request.user:
        return redirect('my_properties')
    
    # Get or create related objects
    try:
        amounts = Amounts.objects.get(apt=apt)
    except Amounts.DoesNotExist:
        amounts = None
    
    try:
        info = Info.objects.get(apt=apt)
    except Info.DoesNotExist:
        info = None
    
    try:
        coords = Coords.objects.get(apt=apt)
    except Coords.DoesNotExist:
        coords = None
    
    images = Images.objects.filter(apt=apt)
    
    if request.method == 'POST':
        apt_form = AptForm(request.POST, instance=apt)
        amounts_form = AmountsForm(request.POST, instance=amounts)
        info_form = InfoForm(request.POST, instance=info)
        coords_form = CoordsForm(request.POST, instance=coords)
        
        if apt_form.is_valid() and amounts_form.is_valid() and info_form.is_valid() and coords_form.is_valid():
            apt_form.save()
            
            amounts_obj = amounts_form.save(commit=False)
            amounts_obj.apt = apt
            amounts_obj.save()
            
            info_obj = info_form.save(commit=False)
            info_obj.apt = apt
            info_obj.save()
            
            coords_obj = coords_form.save(commit=False)
            coords_obj.apt = apt
            coords_obj.save()
            
            return redirect('edit_property', apt_id=apt.id)
    else:
        apt_form = AptForm(instance=apt)
        amounts_form = AmountsForm(instance=amounts)
        info_form = InfoForm(instance=info)
        coords_form = CoordsForm(instance=coords)
    
    return render(request, 'edit_property.html', {
        'apt': apt,
        'apt_form': apt_form,
        'amounts_form': amounts_form,
        'info_form': info_form,
        'coords_form': coords_form,
        'images': images,
    })


@login_required
def add_image(request, apt_id):
    """Add an image to a property"""
    apt = get_object_or_404(Apt, id=apt_id)
    
    if apt.owner != request.user:
        return redirect('my_properties')
    
    if request.method == 'POST':
        form = ImagesForm(request.POST)
        if form.is_valid():
            image = form.save(commit=False)
            image.apt = apt
            image.save()
            return redirect('edit_property', apt_id=apt.id)
    else:
        form = ImagesForm()
    
    return render(request, 'add_image.html', {'apt': apt, 'form': form})


@login_required
def delete_property(request, apt_id):
    """Delete a property"""
    apt = get_object_or_404(Apt, id=apt_id)
    
    if apt.owner != request.user:
        return redirect('my_properties')
    
    if request.method == 'POST':
        apt.delete()
        return redirect('my_properties')
    
    return render(request, 'confirm_delete_property.html', {'apt': apt})


@login_required
def delete_image(request, image_id):
    """Delete an image from a property"""
    image = get_object_or_404(Images, id=image_id)
    apt = image.apt
    
    if apt.owner != request.user:
        return redirect('my_properties')
    
    if request.method == 'POST':
        image.delete()
        return redirect('edit_property', apt_id=apt.id)
    
    return render(request, 'confirm_delete_image.html', {'image': image})