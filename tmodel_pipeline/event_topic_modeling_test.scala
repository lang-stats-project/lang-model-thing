// ===================================================== //
// Event Unsupervised Topic Modeling Scala Script - TEST
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
// Testing parameters
// ===================================================== //

val model_name = args(0);   // same as in train
val testing_csv_file = args(1);
val data_column = 3;
val top_terms = args(2).toInt;

// ===================================================== //
// Setup
// ===================================================== //

val modelPath = file(model_name);

println("Loading "+modelPath);
val model = LoadCVB0LDA(modelPath);

// Load the new dataset for inference...
val source = CSVFile(testing_csv_file);

// Text descriptor
val text = {
	source ~>
	Column(data_column) ~>
	TokenizeWith(model.tokenizer.get)
}

// Base name for output files... 
val output = file(modelPath, source.meta[java.io.File].getName.replaceAll(".csv",""));

// Create dataset to use with LDA
val dataset = LDADataset(text, termIndex = model.termIndex);

// ===================================================== //
// DO INFERENCES 
// ===================================================== //

// Per document distributions over latent topics
println("Writing document distributions to "+output+"-document-topic-distributions.csv");
val perDocTopicDistributions = InferCVB0DocumentTopicDistributions(model,dataset);
CSVFile(output+"-document-topic-distributions.csv").write(perDocTopicDistributions);

println("Writing topic usage to "+output+"-usage.csv");
val usage = QueryTopicUsage(model,dataset,perDocTopicDistributions);
CSVFile(output+"-usage.csv").write(usage);

// Infer per word distributions over latent topics
println("Estimating per-doc per-word topic distributions");
val perDocWordTopicDistributions = EstimatePerWordTopicDistributions(model,dataset,perDocTopicDistributions);

println("Writing top terms to "+output+"-topic-terms.csv");
val topTerms = QueryTopTerms(model,dataset,perDocWordTopicDistributions, numTopTerms=top_terms);
CSVFile(output+"-top-terms.csv").write(topTerms);

// ===================================================== //
// DONE!
// ===================================================== //
