export function emailValidator(email) {
    const re = /\S+@\S+\.\S+/
    if (!email) return "Το Email δεν μπορεί να είναι κενό."
    if (!re.test(email)) return 'Ooops! Χρειάζεται να εισάγετε μια έγκυρη διεύθυνση email.'
    return ''
  }