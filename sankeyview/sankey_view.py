from .augment_view_graph import augment, elsewhere_bundles
from .view_graph import view_graph
from .results_graph import results_graph
from .view_definition import ViewDefinition


def sankey_view(view_definition, dataset, return_unused_flows=False,
                return_bundle_flows=False):

    # Calculate the view graph (adding dummy nodes)
    GV, oV = view_graph(view_definition)

    # Add implicit to/from Elsewhere bundles to the view definition to ensure
    # consistency.
    new_bundles = elsewhere_bundles(view_definition)
    GV2, oV2, new_nodes = augment(GV, oV, new_bundles)

    # XXX messy
    augmented_view = ViewDefinition(dict(view_definition.nodes, **new_nodes),
                                    view_definition.bundles + new_bundles,
                                    view_definition.order,
                                    view_definition.flow_grouping)

    # Get the flows selected by the bundles
    bundle_flows, unused_flows = dataset.apply_view(augmented_view)

    # Calculate the results graph (actual Sankey data)
    GR, oR = results_graph(GV, oV, bundle_flows,
                           flow_grouping=view_definition.flow_grouping)

    result = (GR, oR)
    if return_unused_flows:
        result += (unused_flows,)
    if return_bundle_flows:
        result += (bundle_flows,)
    return result
