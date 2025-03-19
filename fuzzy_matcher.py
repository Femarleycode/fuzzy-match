"""Fuzzy matching application for comparing company data between two datasets."""
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def load_datasets(file1: str, file2: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load the two CSV datasets into pandas DataFrames.
    
    Args:
        file1: Path to the first CSV file
        file2: Path to the second CSV file
        
    Returns:
        Tuple containing two pandas DataFrames
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    return df1, df2

def find_best_match(name: str, choices: List[str], score_cutoff: int = 75) -> Optional[Tuple[str, int]]:
    """Find the best match for a name in a list of choices using fuzzy matching.
    
    Args:
        name: The name to find a match for
        choices: List of possible matches
        score_cutoff: Minimum similarity score to consider a match
        
    Returns:
        Tuple of (best match, similarity score) if found, None otherwise
    """
    match = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    if match and match[1] >= score_cutoff:
        return match
    return None

def match_companies(df1: pd.DataFrame, df2: pd.DataFrame, score_cutoff: int = 75) -> pd.DataFrame:
    """Match companies between two dataframes using fuzzy matching.
    
    Args:
        df1: First DataFrame containing company information
        df2: Second DataFrame containing company information
        score_cutoff: Minimum similarity score to consider a match
        
    Returns:
        DataFrame containing matched companies and their details
    """
    matches: List[Dict[str, Any]] = []
    
    # Get list of company names from df2
    company_names_2 = df2['company_name'].tolist()
    
    # Find matches for each company in df1
    for _, row in df1.iterrows():
        company_1 = row['company_name']
        match = find_best_match(company_1, company_names_2, score_cutoff)
        
        if match:
            company_2, similarity_score = match
            
            # Get the full rows from both dataframes
            df2_row = df2[df2['company_name'] == company_2].iloc[0]
            
            matches.append({
                'company_1': company_1,
                'company_2': company_2,
                'similarity_score': similarity_score,
                'contact_person': row['contact_person'],
                'email': row['email'],
                'industry': df2_row['industry'],
                'revenue': df2_row['revenue'],
                'date_of_birth': row['date_of_birth'],
                'address_1': row['address'],
                'address_2': df2_row['address']
            })
    
    return pd.DataFrame(matches)

def main() -> None:
    """Main function to run the fuzzy matching process."""
    # Load the datasets
    df1, df2 = load_datasets('dataset1.csv', 'dataset2.csv')
    
    # Perform matching
    print("Performing fuzzy matching...")
    matches_df = match_companies(df1, df2)
    
    # Sort by similarity score in descending order
    matches_df = matches_df.sort_values('similarity_score', ascending=False)
    
    # Display results
    print("\nMatching Results:")
    print("=" * 120)
    
    for _, row in matches_df.iterrows():
        print(f"\nMatch Score: {row['similarity_score']}%")
        print(f"Dataset 1: {row['company_1']}")
        print(f"Dataset 2: {row['company_2']}")
        print(f"Contact: {row['contact_person']} ({row['email']})")
        print(f"Industry: {row['industry']}")
        print(f"Revenue: ${row['revenue']}B")
        print(f"Date of Birth: {row['date_of_birth']}")
        print("Address Match:")
        print(f"  Dataset 1: {row['address_1']}")
        print(f"  Dataset 2: {row['address_2']}")
        print("-" * 100)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total number of companies in Dataset 1: {len(df1)}")
    print(f"Total number of companies in Dataset 2: {len(df2)}")
    print(f"Number of matches found: {len(matches_df)}")
    print(f"Average similarity score: {matches_df['similarity_score'].mean():.2f}%")
    print(f"Highest similarity score: {matches_df['similarity_score'].max()}%")
    print(f"Lowest similarity score: {matches_df['similarity_score'].min()}%")
    
    # Save results to CSV
    output_file = 'matched_results.csv'
    matches_df.to_csv(output_file, index=False)
    print(f"\nResults have been saved to {output_file}")

if __name__ == "__main__":
    main() 