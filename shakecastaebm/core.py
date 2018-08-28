from . import damping
from .demand import get_demand
from .damage import get_damage_state_beta, get_damage_probabilities
from .performance_point import performance_point
from .data_tables import pref_periods

def run(capacity, hazard, hazard_beta,
        mag, r_rup, pref_periods=pref_periods):
    '''
    Compares an input capacity curve to a hazard in order to determine
    the probability of a structure being in a specific damage state

    Args:
        capacity: a capacity curve generated by the capacity module
        hazard: spectral curve describing a natural hazard

            [{'x': .01, 'y': .8}, {'x': .02, 'y': 1.1}, ...}]

        hazard_beta: uncertainty in the hazard curve
        pref_periods: a list of periods to interpolate
        mag: magnitude of the earthquake that caused the hazard
        r_rup: closest distance to the rupture surface

    Output:
        damage_probabilities: Probability associated with each damage
            state ex.

        {
            'none': .01,
            'slight': .4,
            'moderate': .55,
            'extensive': .3
            'complete': .1
        }

        capacity: The input capacity curve with additional calculated properties
        demand: The demand curve

        [{
            'x': period,
            'disp': displacement,
            'y': spectral acceleration
        }, ...]

        upper_demand: upper bound demand curve
        lower_demand: lower bound demand curve
        med_intersections: intersections of median capacity and median demand
        lower_intersections: intersections of median capacity and lower demand
        upper_intersections: intersections of median capacity and upper demand

    '''
    demand, lower_demand, upper_demand = get_demand(hazard, hazard_beta, pref_periods, capacity, mag, r_rup)
    med_intersections = performance_point(capacity['curve'], demand)
    lower_intersections = performance_point(capacity['curve'], lower_demand)
    upper_intersections = performance_point(capacity['curve'], upper_demand)

    capacity['calcucated_beta'] = get_damage_state_beta(capacity['default_damage_state_beta'], capacity['damage_state_medians']['complete'], lower_intersections[0]['x'], lower_intersections[0]['y'], upper_intersections[0]['x'], upper_intersections[0]['y'], hazard_beta, capacity['quality_rating'], capacity['performance_rating'], capacity['year'], capacity['stories'])

    damage_probabilities = get_damage_probabilities(capacity['damage_state_medians'], capacity['calcucated_beta'], med_intersections[0]['x'])

    return damage_probabilities, capacity, demand, lower_demand, upper_demand, med_intersections, lower_intersections, upper_intersections
