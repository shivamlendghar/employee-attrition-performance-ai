# ==========================================================
# hr_recommendation.py
#
# Content-Based HR Recommendation
# Uses employee prediction + BM25 retrieval
# ==========================================================

from pathlib import Path
import sys

# Import our existing prediction service
from prediction_service import predict_employee

# Import our existing BM25 search
from bm25_search import bm25_search


# ==========================================================
# CREATE HR QUERY FROM EMPLOYEE ANALYSIS
# ==========================================================

def create_hr_query(
    employee_data,
    prediction_result
):
    """
    Generate an HR knowledge-base query based on
    employee risk and development needs.
    """

    queries = []

    attrition = prediction_result["attrition"]

    performance = prediction_result["performance"]

    # ------------------------------------------------------
    # ATTRITION RISK
    # ------------------------------------------------------

    if attrition["risk"] == "HIGH":

        queries.append(
            "employee wellness work life balance support"
        )

    elif attrition["risk"] == "MEDIUM":

        queries.append(
            "employee engagement workload support"
        )

    # ------------------------------------------------------
    # BURNOUT
    # ------------------------------------------------------

    burnout = float(
        employee_data["burnout_score"]
    )

    if burnout >= 7:

        queries.append(
            "burnout employee assistance wellness"
        )

    # ------------------------------------------------------
    # ENGAGEMENT
    # ------------------------------------------------------

    engagement = float(
        employee_data["engagement_score"]
    )

    if engagement <= 4:

        queries.append(
            "employee engagement support"
        )

    # ------------------------------------------------------
    # MANAGER SUPPORT
    # ------------------------------------------------------

    manager_support = float(
        employee_data["manager_support_score"]
    )

    if manager_support <= 4:

        queries.append(
            "manager support communication"
        )

    # ------------------------------------------------------
    # CAREER DEVELOPMENT
    # ------------------------------------------------------

    years_since_promotion = float(
        employee_data["years_since_promotion"]
    )

    if years_since_promotion >= 4:

        queries.append(
            "promotion career development performance"
        )

    # ------------------------------------------------------
    # PERFORMANCE
    # ------------------------------------------------------

    rating = performance["rating"]

    if rating <= 2:

        queries.append(
            "performance improvement training"
        )

    elif rating == 3:

        queries.append(
            "employee training skill development"
        )

    elif rating == 5:

        queries.append(
            "employee recognition career development"
        )

    # ------------------------------------------------------
    # DEFAULT
    # ------------------------------------------------------

    if not queries:

        queries.append(
            "employee development HR policy"
        )

    # Combine queries
    return " ".join(queries)


# ==========================================================
# REMOVE DUPLICATE DOCUMENTS
# ==========================================================

def remove_duplicates(results):

    seen = set()

    unique_results = []

    for result in results:

        document = result["document"]

        if document in seen:
            continue

        seen.add(document)

        unique_results.append(
            result
        )

    return unique_results


# ==========================================================
# GENERATE RECOMMENDATIONS
# ==========================================================

def recommend_hr_resources(
    employee_data,
    prediction_result,
    top_n=3
):
    """
    Retrieve the most relevant HR documents
    using BM25.
    """

    query = create_hr_query(
        employee_data,
        prediction_result
    )

    print("\nGenerated HR query:")
    print(query)

    # Search using BM25
    results = bm25_search(
        query
    )

    results = remove_duplicates(
        results
    )

    recommendations = []

    for result in results[:top_n]:

        recommendations.append(
            {
                "document": result["document"],
                "score": round(
                    result["score"],
                    4
                )
            }
        )

    return {
        "query": query,
        "recommendations": recommendations
    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("CONTENT-BASED HR RECOMMENDATION")
    print("=" * 70)

    # ------------------------------------------------------
    # Example employee
    # ------------------------------------------------------

    employee = {
        "age": 30,
        "gender": "Male",
        "marital_status": "Single",
        "education_level": "Bachelors",
        "department": "Engineering",
        "job_role": "Data Engineer",
        "job_level": 2,
        "monthly_income": 50000,
        "stock_option_level": 1,
        "salary_hike_pct": 12,
        "years_at_company": 3,
        "total_working_years": 6,
        "years_since_promotion": 4,
        "num_prior_companies": 2,
        "work_mode": "Hybrid",
        "commute_minutes": 35,
        "overtime_hours_per_week": 15,
        "business_travel_days_per_year": 10,
        "training_hours": 10,
        "manager_support_score": 4,
        "burnout_score": 8,
        "engagement_score": 4,
        "work_life_balance_score": 4,
        "performance_rating": 3,
        "last_review_score": 6,
        "uses_ai_tools_at_work": True,
        "perceived_ai_job_risk": 6,
    }

    # ------------------------------------------------------
    # Run prediction
    # ------------------------------------------------------

    prediction = predict_employee(
        employee
    )

    print("\nPrediction:")

    print(
        f"Attrition Risk: "
        f"{prediction['attrition']['risk']}"
    )

    print(
        f"Attrition Probability: "
        f"{prediction['attrition']['percentage']}%"
    )

    print(
        f"Performance Rating: "
        f"{prediction['performance']['rating']}"
    )

    # ------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------

    result = recommend_hr_resources(
        employee,
        prediction,
        top_n=3
    )

    print("\n" + "=" * 70)
    print("RECOMMENDED HR RESOURCES")
    print("=" * 70)

    if not result["recommendations"]:

        print(
            "No relevant HR resources found."
        )

    else:

        for index, recommendation in enumerate(
            result["recommendations"],
            start=1
        ):

            print(
                f"\n{index}. "
                f"{recommendation['document']}"
            )

            print(
                f"   BM25 Score: "
                f"{recommendation['score']}"
            )

    print("\n" + "=" * 70)
    print("RECOMMENDATION MODULE COMPLETED")
    print("=" * 70)