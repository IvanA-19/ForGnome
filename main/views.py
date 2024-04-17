from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, AddressForm
from .models import Restaurant, FoodPositions, DrinkPositions, Order, Address


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def restaurants(request):
    restaurants = Restaurant.objects.order_by('name')
    context = {'restaurants': restaurants}

    return render(request, 'main/restaurants.html', context)


def restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    context = {'restaurant': restaurant}

    return render(request, 'main/restaurant.html', context)


def food(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    food = restaurant.foodpositions_set.order_by('name')

    context = {'restaurant': restaurant, 'food': food}
    return render(request, 'main/food.html', context)


@login_required
def dish(request, restaurant_id, dish_id,):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    dish = restaurant.foodpositions_set.get(id=dish_id)

    if request.method != 'POST':
        form = OrderForm()
    else:
        form = OrderForm(data=request.POST)

        new_order = form.save(commit=False)
        new_order.position = dish.name
        new_order.price = dish.price
        new_order.buyer = request.user
        form.save()

        return redirect('main:restaurant', restaurant_id)

    context = {'dish': dish, 'form': form}

    return render(request, 'main/dish.html', context)


@login_required
def drink(request, restaurant_id, drink_id,):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    drink = restaurant.drinkpositions_set.get(id=drink_id)

    if request.method != 'POST':
        form = OrderForm()
    else:
        form = OrderForm(data=request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.position = drink.name
            new_order.price = drink.price
            if new_order.count < 0:
                new_order.count = 0
            print(request.user)
            new_order.buyer = request.user
            form.save()

            return redirect('main:restaurant', restaurant_id)

    context = {'drink': drink, 'form': form}

    return render(request, 'main/drink.html', context)


def drinks(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    drinks = restaurant.drinkpositions_set.order_by('name')

    context = {'restaurant': restaurant, 'drinks': drinks}
    return render(request, 'main/drinks.html', context)


@login_required
def cart(request):
    buyer = request.user
    positions = Order.objects.filter(buyer_id=buyer.id)
    final_price = sum(pos.count * pos.price for pos in positions)
    address = Address.objects.filter(user_id=request.user.id)

    if request.method != 'POST':
        form = AddressForm()
    else:
        form = AddressForm(data=request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            if new_address in address:
                new_address.user = request.user
                form.save()

            send_mail(
                f"Заказ для {buyer}",
                f"Спасибо за ваш заказ! Ожидайте доставку в течение 2 часов."
                f"\nСумма заказа: {final_price}\nСостав заказа:\n" +
                '\n'.join(f'{pos} {pos.count} шт.' for pos in positions),
                "KabanDelivery@gmail.com",
                [f"{buyer.email}"],
                fail_silently=False,
            )
            positions.delete()
            return redirect('main:ordered')
    context = {'buyer': buyer, 'order': positions, 'final_price': final_price, 'form': form}
    return render(request, 'main/cart.html', context)


def ordered(request):
    return render(request, 'main/ordered.html')


@login_required
def edit(request, pos_id):
    position = Order.objects.get(id=pos_id)
    if request.method != 'POST':
        form = OrderForm(instance=position)
    else:
        form = OrderForm(instance=position, data=request.POST)
        if form.is_valid():
            form.count = request.POST
            form.save()
            if int(form.count['count']) == 0:
                position.delete()
        return redirect('main:cart')

    context = {'position': position, 'form': form}

    return render(request, 'main/edit.html', context)
