# games/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Game

@login_required
def game_list(request):
    """
    Display list of all active Tic Tac Toe games
    """
    active_games = Game.objects.filter(game_state='active').order_by('-created_at')
    return render(request, 'games/game_list.html', {'games': active_games})

@login_required
def new_game(request):
    """
    Create a new Tic Tac Toe game with unique room name
    """
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        
        if not room_name:
            return render(request, 'games/new_game.html', {
                'error': "Room name cannot be empty."
            })
        
        try:
            game = Game.objects.create(
                room_name=room_name,
                owner=request.user,
                board=' ' * 9,
                active_player=Game.PLAYER_1,
                game_state=Game.STATUS_ACTIVE
            )
            return redirect('game_detail', game_id=game.id)
            
        except IntegrityError:
            return render(request, 'games/new_game.html', {
                'error': f"Room name '{room_name}' already exists. Please choose a different name."
            })
    
    return render(request, 'games/new_game.html')

@login_required
def game_detail(request, game_id):
    """
    Display game board
    """
    game = get_object_or_404(Game, id=game_id)
    board = game.get_board_as_list()
    is_owner = request.user == game.owner
    
    context = {
        'game': game,
        'board': board,
        'is_owner': is_owner,
    }
    
    return render(request, 'games/game_detail.html', context)

@login_required
def make_move_view(request, game_id):
    """
    Handle player moves
    """
    game = get_object_or_404(Game, id=game_id)
    
    if request.method == 'POST':
        if game.game_state == Game.STATUS_ACTIVE:
            if request.user == game.owner:
                position = request.POST.get('position')
                
                if position is not None:
                    try:
                        position = int(position)
                        if 0 <= position <= 8:
                            player_symbol = 'X' if game.active_player == Game.PLAYER_1 else 'O'
                            
                            if game.make_move(position, player_symbol):
                                result = game.check_winner()
                                if result:
                                    if result == 'tie':
                                        game.game_state = Game.STATUS_TIE
                                    else:
                                        game.game_state = Game.STATUS_WON
                                        game.winner = Game.PLAYER_1 if result == 'X' else Game.PLAYER_2
                                else:
                                    game.active_player = Game.PLAYER_2 if game.active_player == Game.PLAYER_1 else Game.PLAYER_1
                                
                                game.save()
                    except ValueError:
                        pass
    
    return redirect('game_detail', game_id=game_id)

@login_required
def delete_game(request, game_id):
    """
    Delete a game
    """
    game = get_object_or_404(Game, id=game_id)
    
    if request.user == game.owner:
        game.delete()
    
    return redirect('game_list')