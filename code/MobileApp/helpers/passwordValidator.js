export function passwordValidator(password) {
    if (!password) return "Το password δεν μπορεί να είναι κενό."
    if (password.length < 5) return 'Το password πρέπει να περιέχει τουλάχιστον 5 χαρακτήρες.'
    return ''
  }