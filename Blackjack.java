package blackjack;
import java.util.*;

public class Blackjack implements BlackjackEngine {
	
	
	private ArrayList<Card> gameDeck;
	private ArrayList<Card> dealerCards;
	private ArrayList<Card> playerCards;
	private int numDecks;
	private Random randomSeed;
	private int account;
	private int bet;
	private int gameStatus;
	
	/**
	 * Constructor you must provide.  Initializes the player's account 
	 * to 200 and the initial bet to 5.  Feel free to initialize any other
	 * fields. Keep in mind that the constructor does not define the 
	 * deck(s) of cards.
	 * @param randomGenerator
	 * @param numberOfDecks
	 */
	public Blackjack() {
		account = 200;
		bet = 5;
	}
	
	public Blackjack(Random randomGenerator, int numberOfDecks) {
	    this();
	    numDecks = numberOfDecks;
	    randomSeed = randomGenerator;
	}
	
	public int getNumberOfDecks() {
		return numDecks;
	}
	
	public void createAndShuffleGameDeck() {
		gameDeck = new ArrayList<Card>();
		dealerCards = new ArrayList<Card>();
		playerCards = new ArrayList<Card>();
		for (int i = 0; i < numDecks; i++) {
	    	for (CardSuit suit : CardSuit.values()) {
	    		for ( CardValue value : CardValue.values()) {
	    			gameDeck.add(new Card(value, suit));
	    		}
	    	}
	    }
		Collections.shuffle(gameDeck, randomSeed);
	}
	
	public Card[] getGameDeck() {
		return cardArrayListToArray( gameDeck);
	}
	
	public void deal() {
		createAndShuffleGameDeck();
		
		playerCards.add(dealCard(true));
		dealerCards.add(dealCard(false));
		playerCards.add(dealCard(true));
		dealerCards.add(dealCard(true));
		
		gameStatus = 8;
		
		account -= bet;
	}
		

	public Card[] getDealerCards() {
		return cardArrayListToArray( dealerCards);
	}

	public int[] getDealerCardsTotal() {
		return stripBust(getCardsTotal(cardsToValues(getDealerCards())));
	}
	

	public int getDealerCardsEvaluation() {
		return cardEvaluation(getDealerCardsTotal(), dealerCards.size());
	}
	
	public Card[] getPlayerCards() {
		return cardArrayListToArray( playerCards);
	}
	
	public int[] getPlayerCardsTotal() {
		return stripBust(getCardsTotal(cardsToValues(getPlayerCards())));
	}
		
	public int getPlayerCardsEvaluation() {
		return cardEvaluation(getPlayerCardsTotal(), playerCards.size());
	}
	
	public void playerHit() {
		playerCards.add(dealCard(true));
		if (getPlayerCardsEvaluation() == 3) {
			gameStatus = 6;
		}
		
	}
	
	public void playerStand() {
		dealerCards.get(0).setFaceUp();
		while (getDealerCardsTotal() != null && getDealerCardsTotal()[getDealerCardsTotal().length - 1] < 16) {
			dealerCards.add(dealCard(true));
		}
		
		if (getDealerCardsTotal() == null) {
			gameStatus = 7;
			account += 2*bet;
			return;
		}
		int dealerTotal = getDealerCardsTotal()[getDealerCardsTotal().length - 1];
		int playerTotal = getPlayerCardsTotal()[getPlayerCardsTotal().length - 1];
		if (dealerTotal > playerTotal) {
			gameStatus = 6;
		}
		else if (dealerTotal < playerTotal) {
			account += 2*bet;
			gameStatus = 7;
		}
		else {		
			account += bet;
			gameStatus = 1;
		}
	}
	
	public int getGameStatus() {
		return gameStatus;
	}
		
	public void setBetAmount(int amount) {
		bet = amount;
	}
	
	public int getBetAmount() {
		return bet;
	}
	
	public void setAccountAmount(int amount) {	
		account = amount;
	}
	
	public int getAccountAmount() {
		return account;
	}
	
	/* Feel Free to add any private methods you might need */
	
	/**
	 * Treats an Ace as 1
	 * 
	 * @param Array of type Card 
	 * @return Array of primitive type int, representing the corresponding card values
	 */
	
	private int[] cardsToValues( Card[] cards) {
		int[] valueArray = new int[cards.length];
		for (int i=0; i < cards.length; i++) {
			valueArray[i] = cards[i].getValue().getIntValue();
		}
		return valueArray;
	}
	
	/**
	 * This method is called recursively on Ace as 1, 
	 * passing back a copy of the cards with Ace high instead, 
	 * until all unique non ordered combinations of aces have been dealt with
	 * The list should be sorted low to high since the base case results
	 * in all aces being high and each new value gets added to the front
	 * 
	 * @param can array of primitive type int cards with the value of cards
	 * @return all possible combinations of total values of the given cards
	 */
	private int[] getCardsTotal( int[] cards) {
		ArrayList<Integer> values = new ArrayList<Integer>();
		int value = 0;
		for(int i = 0; i < cards.length; i++) {
			if (cards[i] == 1) {
				int[] newCards = cards.clone();
				newCards[i] = 11;
				for (int j : getCardsTotal(newCards)) {
					values.add(j);
				}
			}
			value += cards[i];
		}
		values.add(0, value);
		return intArrayListToArray(values);
	}
	
	/**
	 * For some reason this method doesn't already exist somewhere
	 * Maybe it does and I just can't find it...
	 * 
	 * @param an array list of type Integer
	 * @return an array of primitive type int
	 */
	private int[] intArrayListToArray(ArrayList<Integer> list) {
		int[] array = new int[list.size()];	
		for( int i=0; i < list.size(); i++) {
			array[i] = list.get(i).intValue(); 
		}
		return array;
	}
	
	
	/**
	 * Similarly to the above method, 
	 * Copies Cards from an ArrayList to an array
	 * @param list
	 * @return
	 */
	private Card[] cardArrayListToArray(ArrayList<Card> list) {
		Card[] array = new Card[list.size()];	
		for( int i=0; i < list.size(); i++) {
			array[i] = list.get(i); 
		}
		
		return array;
	}
	
	/**
	 * returns the card at the top of the deck,
	 * while removing it from the deck and 
	 * assigning its 'facing' boolean
	 * @param faceUp
	 * @return
	 */
	private Card dealCard(boolean faceUp) {
		Card card = gameDeck.get(0);
		gameDeck.remove(0);
		if (!faceUp) {
			card.setFaceDown();
		}
		return card;
	}
	
	
	/**
	 * This method will take in an int array of the card totals
	 * and will remove any values above 21,
	 * returning either null or a shorter array
	 * @param cardTotals
	 * @return
	 */
	private int[] stripBust(int[] cardTotals) {
		int validValues=0;
		for (int i =0; i < cardTotals.length; i++) {
			if (cardTotals[i] <= 21) {
				validValues++;
			}
		}
		if(validValues > 0) {
			int[] totals = new int[validValues];
			for (int i = 0; i < validValues; i++) {
				totals[i] = cardTotals[i];
			}
			return totals;
		}
		else {
			return null;
		}
	}
	
	/**
	 * Given the totals and the number of cards, 
	 * this method will evaluate the hand based on the game rules and return the result
	 * 
	 * @param totals
	 * @param numCards
	 * @return
	 */
	private int cardEvaluation(int[] totals, int numCards) {
		if (totals == null) {
			return 3;
		}
		
		else {
			for (int total : totals) {
				if (total == 21) {
					if(numCards == 2) {
						return 4;
					}
					else {
						return 5;
					}
				}
			}
			return 2;
		}
	}
}