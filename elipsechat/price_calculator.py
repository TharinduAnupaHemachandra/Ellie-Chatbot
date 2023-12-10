import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def price_calculator(input, output, input_price_per_thousand, output_price_per_thousand, profit, db, session_id):
  input_tokens = encoding.encode(input)
  input_tokens_count = len(input_tokens)

  output_tokens = encoding.encode(output)
  output_tokens_count = len(output_tokens)

  N_input = input_tokens_count / 1000

  N_output = output_tokens_count / 1000

  total_input_price = N_input * input_price_per_thousand

  total_output_price = N_output * output_price_per_thousand

  final_price_one = total_input_price + total_output_price

  doc_ref = db.collection("price_data").document(session_id)

  document = doc_ref.get()

  old_final_price = document.get("final_price")
  old_final_price_with_profit = document.get("final_price_with_profit")

  if old_final_price == None:
    final_price = 0 + final_price_one
  else:
    final_price = old_final_price + final_price_one

  if old_final_price_with_profit ==  None:
    final_price_with_profit = 0 + (final_price_one * profit)
  else:
    final_price_with_profit = old_final_price_with_profit + (final_price_one * profit)

  updated_data = {
    "session_id": session_id,
    "final_price": final_price,
    "final_price_with_profit": final_price_with_profit,
    # Add more fields to update
  }

  if document.exists:
    price_data = document.to_dict()

    print(price_data)

  else:
    # If the document does not exist, create a new one with the given ID and values
    db.collection("price_data").document(session_id).set(updated_data)

    print(f"Document '{session_id}' created with values.")

  print("Updated Data")
  print(updated_data)
  doc_ref.update(updated_data)

  return final_price * profit