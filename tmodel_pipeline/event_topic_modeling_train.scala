// ===================================================== //
// Event Unsupervised Topic Modeling Scala Script - TRAIN
// ===================================================== //
import scalanlp.io._;
import scalanlp.stage._;
import scalanlp.stage.text._;
import scalanlp.text.tokenize._;
import scalanlp.pipes.Pipes.global._;

import edu.stanford.nlp.tmt.stage._;
import edu.stanford.nlp.tmt.model.lda._;
import edu.stanford.nlp.tmt.model.llda._;

// ===================================================== //
// SETUP PARAMETERS
// ===================================================== //

// Name of the input csv training file
val training_csv_file = args(1);
println("Training csv file: " + training_csv_file)

val model_name = args(0);
println("Model name: " + model_name)

val num_topics_to_find = args(2).toInt;
println("Num topics to find: " + num_topics_to_find)

val max_iter = args(3).toInt;
println("Max iterations: " + max_iter)

val id_column = 1;
println("Id column: " + id_column)

val data_column = 3;
println("Data column: " + data_column)

val min_token_length = args(4).toInt;
println("Min token length: " + min_token_length)

val min_doc_count = 1; 
println("Min num docs to process: " + min_doc_count)

val stop_words = args(5).toInt;
println("Num stop words: " + stop_words)

val min_doc_length = args(6).toInt;
println("Min words in doc: " + min_doc_length)

val smoothing = 0.01;

// Assume the ID for the item is the first column
println("Setting up csv file...")
val source = CSVFile(training_csv_file) ~> IDColumn(id_column);


// String line tokenizer... basic english, all lowercase, etc.
println("Setting up tokenizer...")
val tokenizer = {
	SimpleEnglishTokenizer() ~>				// use English words
	CaseFolder() ~>							// make everything lowercase
	StopWordFilter("en") ~>					// remove stop words... 
	WordsAndNumbersOnlyFilter() ~>			// remove all punctuation
	MinimumLengthFilter(min_token_length)	// tokens must be at least 2 chars long
}

// Text Description -- all data is in Column 5 (index starts at 1)
println("Setting up text parser...")
val text = {
	source ~>											// training CSV file
	Column(data_column) ~>								// data is in column 5 of the training file
	TokenizeWith(tokenizer) ~>							// specify that text should be parsed with above tokenizer
	TermCounter() ~>									// count total number of terms (standard algorithm)
	TermMinimumDocumentCountFilter(min_doc_count) ~>	// limit topic words to things that appear at least 4 times (standard algorithtm)
	TermDynamicStopListFilter(stop_words) ~>			// filter out the top 30 stop words (standard)
	DocumentMinimumLengthFilter(min_doc_length)			// document must have at least 5 tokens for us to consider it (standard)
}
println("Done setting up variables...")

// ===================================================== //
// TRAIN THE MODEL
// ===================================================== //

// Dataset to use with LDA model
println("Reading dataset...")
val dataset = LDADataset(text);

// Define the model parameters
println("Setting up model...")
val params = LDAModelParams(numTopics = num_topics_to_find, dataset = dataset,
		topicSmoothing = smoothing, termSmoothing = smoothing);

// Where to output the model when finished...
println("Creating model directory...")
val modelPath = file(model_name);

// Train the topic model, write everything to output folder...
println("Starting to train LDA model...")
TrainCVB0LDA(params, dataset, output=modelPath, maxIterations=max_iter);
println("Finished training LDA model!")

// Output keywords
println("Terms in the stop list:");
for (term <- text.meta[TermStopList]) {
  println("  " + term);
}
// ===================================================== //
// DONE
// ===================================================== //

