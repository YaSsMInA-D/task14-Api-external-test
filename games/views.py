from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse  # Returns HTTP responses in JSON format (
from .models import Game 

@login_required
def game_list(request):
    """
    Display list of active Tic Tac Toe games with button to start new game
    """
    games = Game.objects.all().order_by('-created_at')   #descender
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def create_game(request):
    """
    Create a new Tic Tac Toe game - user only enters room name
    """
    if request.method == 'POST':  #- HTTP method check - handles form submission
        room_name = request.POST.get('room_name', '').strip()  #- Get room name from form       
        if not room_name:            #Validation check for empty room name
            messages.error(request, 'Room name is required')
            return render(request, 'games/create_game.html')
        
        # Check if room name already exists
        if Game.objects.filter(room_name=room_name).exists():
            messages.error(request, 'A game with this room name already exists')
            return render(request, 'games/create_game.html')
        
        # Create the game - only room name is provided by user
        game = Game.objects.create(
            room_name=room_name,
            owner=request.user,  #- Set the owner of the game
            board=' ' * 9,  
            current_player=Game.PLAYER_X,  # Player X starts
            game_state=Game.STATE_ACTIVE  
        )
        
        messages.success(request, f'Game "{room_name}" created successfully!') 
        return redirect('games:game_detail', game_id=game.id)  #
    
    return render(request, 'games/create_game.html')

@login_required
def game_detail(request, game_id):
    """
    Show game at current state with grid
    Game logic moved to WebSocket consumer
    """
    game = get_object_or_404(Game, id=game_id) #
    
    # Handle joining the game
    if request.method == 'POST' and 'join_game' in request.POST:  #Checks if user clicked "Join Game" button.
        if game.player_o is None and request.user != game.owner:
            success, message = game.join_game(request.user)
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
        return redirect('games:game_detail', game_id=game.id)
    
    # Prepare game data for WebSocket
    game_data = game.get_game_data()
    game_data['current_user'] = request.user.username
    game_data['is_player'] = game.is_player(request.user)
    game_data['player_symbol'] = game.get_player_symbol(request.user)
    
    context = {
        'game': game,
        'board_display': game.get_board_display(),
        'game_data': game_data,  # Pass data to template for WebSocket
    }
    return render(request, 'games/game_detail.html', context)

@login_required
def delete_game(request, game_id):
    """
    Delete game (close the room) - only owner can delete
    """
    game = get_object_or_404(Game, id=game_id)
    
    # Only owner can delete their game
    if game.owner != request.user:  #Ensures users can only delete
        messages.error(request, 'You can only delete your own games')
        return redirect('games:game_list')
    
    room_name = game.room_name
    game.delete()
    messages.success(request, f'Game "{room_name}" has been deleted')
    
    return redirect('games:game_list')

@login_required
def join_game(request, game_id):
    """
    API to join a game
    """
    game = get_object_or_404(Game, id=game_id)  # gets the game or returns 404
    
    if game.player_o is None and request.user != game.owner:  # Checks if the second player is available 
        success, message = game.join_game(request.user)
        if success:                                        #Calls join_game() method, returns JSON response (success/error)
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return JsonResponse({'status': 'error', 'message': message})
    
    return JsonResponse({'status': 'error', 'message': 'Cannot join this game'}) 